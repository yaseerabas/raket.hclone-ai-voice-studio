# app/routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.models.plan import Plan
from app.models.usage import Usage
from app.models.audio_file import AudioFile
from app.models.contact_message import ContactMessage
from app import db
from werkzeug.security import generate_password_hash
from app.schemas.user_schema import UserSchema
from app.schemas.plan_schema import PlanSchema
from app.schemas.usage_schema import UsageSchema
from app.schemas.contact_message_schema import ContactMessageSchema
from datetime import datetime

admin_bp = Blueprint('admin', __name__)
user_schema = UserSchema()
plan_schema = PlanSchema()
usage_schema = UsageSchema()
contact_schema = ContactMessageSchema()

# Decorator to allow only admin
def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            identity = get_jwt_identity()
            if not identity:
                return jsonify({"error": "Invalid token"}), 401
                
            user = User.query.get(int(identity))
            if not user or user.user_type != 'admin':
                return jsonify({"error": "Admin access required"}), 403
                
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 401
    wrapper.__name__ = fn.__name__
    return wrapper

# Assign plan to user - Simple version without admin check for testing
@admin_bp.route('/assign-plan', methods=['POST', 'OPTIONS'])
def assign_plan():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # First create default plans if they don't exist
        plans_data = [
            {"name": "Basic", "character_limit": 10000},
            {"name": "Pro", "character_limit": 50000},
            {"name": "Premium", "character_limit": 100000},
            {"name": "Enterprise", "character_limit": 500000}
        ]
        
        for plan_data in plans_data:
            existing = Plan.query.filter_by(name=plan_data['name']).first()
            if not existing:
                plan = Plan(
                    name=plan_data['name'],
                    character_limit=plan_data['character_limit']
                )
                db.session.add(plan)
        
        db.session.commit()
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        email = data.get('email')
        plan_id = data.get('plan_id')
        
        if not email or not plan_id:
            return jsonify({"error": "Email and plan_id required"}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        # Update user plan
        user.plan_id = plan.id
        user.updated_at = datetime.utcnow()
        
        # Create or update subscription
        from app.models.subscription import Subscription
        from datetime import timedelta
        
        subscription = Subscription.query.filter_by(user_id=user.id, status='active').first()
        if subscription:
            subscription.plan_id = plan.id
            subscription.updated_at = datetime.utcnow()
        else:
            # Set expiry date 30 days from now
            end_date = datetime.utcnow() + timedelta(days=30)
            subscription = Subscription(
                user_id=user.id,
                plan_id=plan.id,
                status='active',
                start_date=datetime.utcnow(),
                end_date=end_date
            )
            db.session.add(subscription)
        
        # Update or create usage
        usage = Usage.query.filter_by(user_id=user.id).first()
        if usage:
            usage.characters_remaining = plan.character_limit
            usage.characters_used = 0
        else:
            usage = Usage(
                user_id=user.id, 
                characters_remaining=plan.character_limit,
                characters_used=0
            )
            db.session.add(usage)
            
        db.session.commit()
        
        return jsonify({
            "message": f"Plan '{plan.name}' assigned to {user.email}",
            "user_id": user.id,
            "plan_name": plan.name,
            "character_limit": plan.character_limit
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Reset user password (admin only)
@admin_bp.route('/reset-password', methods=['POST'])
@admin_required
def reset_password():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_password = data.get('new_password')
        if not new_password:
            return jsonify({"error": "New password required"}), 400

        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": f"Password reset for {user.email}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Admin Stats
@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    try:
        total_users = User.query.filter_by(user_type='user').count()
        total_admins = User.query.filter_by(user_type='admin').count()
        total_plans = Plan.query.count()
        total_audios = AudioFile.query.count()
        
        # Active users (users with plans)
        active_users = User.query.filter(User.plan_id.isnot(None)).count()
        
        # Recent registrations (last 30 days)
        from datetime import timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_users = User.query.filter(User.created_at >= thirty_days_ago).count()
        
        # Total characters used
        total_chars_used = db.session.query(db.func.sum(Usage.characters_used)).scalar() or 0
        
        return jsonify({
            "total_users": total_users,
            "total_admins": total_admins,
            "active_users": active_users,
            "total_plans": total_plans,
            "total_audios": total_audios,
            "recent_users": recent_users,
            "total_characters_used": total_chars_used,
            "last_updated": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get All Users with pagination and search
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        
        query = User.query
        
        # Search filter
        if search:
            query = query.filter(User.email.contains(search))
            
        # Pagination
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for user in users.items:
            user_data = {
                "id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                "plan_id": user.plan_id,
                "plan_name": user.plan.name if user.plan else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "usage": {
                    "characters_used": user.usage.characters_used if user.usage else 0,
                    "characters_remaining": user.usage.characters_remaining if user.usage else 0
                } if user.usage else None
            }
            result.append(user_data)
            
        return jsonify({
            "users": result,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": users.total,
                "pages": users.pages,
                "has_next": users.has_next,
                "has_prev": users.has_prev
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update User
@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        # Update user fields
        if 'user_type' in data:
            user.user_type = data['user_type']
            
        # Update password if provided
        if 'password' in data and data['password']:
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(data['password'])
            
        if 'plan_id' in data:
            plan_id = data['plan_id']
            if plan_id:
                plan = Plan.query.get(plan_id)
                if not plan:
                    return jsonify({"error": "Plan not found"}), 404
                user.plan_id = plan_id
                
                # Update usage when plan changes
                usage = Usage.query.filter_by(user_id=user.id).first()
                if usage:
                    usage.characters_remaining = plan.character_limit
                    usage.characters_used = 0
                else:
                    usage = Usage(
                        user_id=user.id,
                        characters_remaining=plan.character_limit,
                        characters_used=0
                    )
                    db.session.add(usage)
            else:
                user.plan_id = None
        
        # Update subscription status if provided
        if 'status' in data or 'start_date' in data or 'end_date' in data:
            from app.models.subscription import Subscription
            subscription = Subscription.query.filter_by(user_id=user.id).first()
            
            if subscription:
                if 'status' in data:
                    subscription.status = data['status'].lower()
                if 'start_date' in data and data['start_date']:
                    subscription.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
                if 'end_date' in data and data['end_date']:
                    subscription.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
                subscription.updated_at = datetime.utcnow()
            else:
                # Create new subscription if doesn't exist
                from datetime import timedelta
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d') if data.get('start_date') else datetime.utcnow()
                end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') if data.get('end_date') else start_date + timedelta(days=30)
                
                subscription = Subscription(
                    user_id=user.id,
                    plan_id=user.plan_id,
                    status=data.get('status', 'active').lower(),
                    start_date=start_date,
                    end_date=end_date
                )
                db.session.add(subscription)
                
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                "plan_id": user.plan_id
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete User
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Prevent deleting admin users
        if user.user_type == 'admin':
            return jsonify({"error": "Cannot delete admin users"}), 403
            
        user_email = user.email
        
        # Delete related records first (cascade delete)
        Usage.query.filter_by(user_id=user_id).delete()
        AudioFile.query.filter_by(user_id=user_id).delete()
        
        # Delete user
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "message": f"User {user_email} deleted successfully",
            "deleted_user_id": user_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Create Plan (Remove admin_required for frontend access)
@admin_bp.route('/plans', methods=['POST'])
def create_plan():
    try:
        data = request.get_json()
        if isinstance(data, list):
            # Batch create
            plans = []
            for plan_data in data:
                plan = Plan(
                    name=plan_data['name'],
                    character_limit=plan_data['character_limit']
                )
                db.session.add(plan)
                plans.append(plan)
            db.session.commit()
            return jsonify({"message": f"{len(plans)} plans created"}), 201
        else:
            # Single create
            if not data.get('name') or not data.get('character_limit'):
                return jsonify({"error": "Name and character_limit required"}), 400
                
            plan = Plan(
                name=data['name'],
                character_limit=data['character_limit']
            )
            db.session.add(plan)
            db.session.commit()
            return jsonify({"message": "Plan created", "plan_id": plan.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update Plan (Remove admin_required for frontend access)
@admin_bp.route('/plans/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id):
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        plan.name = data.get('name', plan.name)
        plan.character_limit = data.get('character_limit', plan.character_limit)
        db.session.commit()
        return jsonify({"message": "Plan updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete Plan (Remove admin_required for frontend access)
@admin_bp.route('/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        # Check if any users are using this plan
        users_count = User.query.filter_by(plan_id=plan_id).count()
        if users_count > 0:
            return jsonify({"error": f"Cannot delete plan. {users_count} users are using this plan."}), 400

        db.session.delete(plan)
        db.session.commit()
        return jsonify({"message": "Plan deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get Recent Activity
@admin_bp.route('/recent-activity', methods=['GET'])
def get_recent_activity():
    try:
        from app.models.subscription import Subscription
        
        limit = request.args.get('limit', 5, type=int)
        
        # Get recent subscriptions with user and plan details
        recent_subscriptions = db.session.query(Subscription, User, Plan).join(
            User, Subscription.user_id == User.id
        ).join(
            Plan, Subscription.plan_id == Plan.id
        ).order_by(Subscription.created_at.desc()).limit(limit).all()
        
        activity = []
        
        # Add subscription activities
        for subscription, user, plan in recent_subscriptions:
            activity.append({
                "type": "subscription_created",
                "description": f"New subscription: {user.email} - {plan.name} Plan activated",
                "timestamp": subscription.created_at.isoformat() if subscription.created_at else None,
                "user_id": user.id,
                "user_email": user.email,
                "plan_name": plan.name,
                "subscription_id": subscription.id,
                "status": subscription.status
            })
            
        return jsonify({
            "activity": activity,
            "total_items": len(activity)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get Contact Messages with pagination
@admin_bp.route('/messages', methods=['GET'])
@admin_required
def get_messages():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', 'all', type=str)
        
        query = ContactMessage.query
        
        # Filter by status if needed (assuming you add status field later)
        # if status != 'all':
        #     query = query.filter_by(status=status)
            
        messages = query.order_by(ContactMessage.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for msg in messages.items:
            result.append({
                "id": msg.id,
                "name": msg.name,
                "email": msg.email,
                "subject": msg.subject,
                "message": msg.message,
                "created_at": msg.created_at.isoformat() if msg.created_at else None
            })
            
        return jsonify({
            "messages": result,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": messages.total,
                "pages": messages.pages,
                "has_next": messages.has_next,
                "has_prev": messages.has_prev
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get All Plans (Remove admin_required for frontend access)
@admin_bp.route('/plans', methods=['GET'])
def get_plans():
    try:
        plans = Plan.query.order_by(Plan.created_at.desc()).all()
        result = []
        for plan in plans:
            # Count users with this plan
            user_count = User.query.filter_by(plan_id=plan.id).count()
            result.append({
                "id": plan.id,
                "name": plan.name,
                "character_limit": plan.character_limit,
                "user_count": user_count,
                "created_at": plan.created_at.isoformat() if plan.created_at else None
            })
        return jsonify({"plans": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test endpoint for debugging
@admin_bp.route('/test', methods=['GET', 'POST'])
def test_admin():
    try:
        print(f"Test endpoint called with method: {request.method}")
        print(f"Headers: {dict(request.headers)}")
        if request.method == 'POST':
            data = request.get_json()
            print(f"POST data: {data}")
        return jsonify({"message": "Admin test endpoint working", "method": request.method}), 200
    except Exception as e:
        print(f"Error in test endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Test endpoint with JWT
@admin_bp.route('/test-jwt', methods=['GET', 'POST'])
@jwt_required()
def test_admin_jwt():
    try:
        identity = get_jwt_identity()
        print(f"JWT test - Identity: {identity}")
        return jsonify({"message": "JWT test working", "user_id": identity}), 200
    except Exception as e:
        print(f"Error in JWT test: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Test endpoint with admin check
@admin_bp.route('/test-admin', methods=['GET', 'POST'])
@admin_required
def test_admin_check():
    try:
        identity = get_jwt_identity()
        return jsonify({"message": "Admin test working", "admin_id": identity}), 200
    except Exception as e:
        print(f"Error in admin test: {str(e)}")
        return jsonify({"error": str(e)}), 500
# Simple test endpoint
@admin_bp.route('/test-simple', methods=['POST', 'OPTIONS'])
def test_simple():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        return jsonify({"message": "Test working", "received_data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Create default plans
@admin_bp.route('/create-default-plans', methods=['POST'])
def create_default_plans():
    try:
        plans_data = [
            {"name": "Basic", "character_limit": 10000},
            {"name": "Pro", "character_limit": 50000},
            {"name": "Premium", "character_limit": 100000}
        ]
        
        created_plans = []
        for plan_data in plans_data:
            existing = Plan.query.filter_by(name=plan_data['name']).first()
            if not existing:
                plan = Plan(
                    name=plan_data['name'],
                    character_limit=plan_data['character_limit']
                )
                db.session.add(plan)
                created_plans.append(plan_data['name'])
        
        db.session.commit()
        return jsonify({
            "message": "Default plans created",
            "created": created_plans
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Create admin user
@admin_bp.route('/create-admin', methods=['POST'])
def create_admin():
    try:
        from werkzeug.security import generate_password_hash
        
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                user_type='admin'
            )
            db.session.add(admin)
            db.session.commit()
            return jsonify({"message": "Admin created: admin@example.com / admin123"}), 200
        else:
            return jsonify({"message": "Admin already exists"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
# Get subscription users with details
@admin_bp.route('/subscription-users', methods=['GET'])
def get_subscription_users():
    try:
        from app.models.subscription import Subscription
        
        # Get all users with their subscriptions
        users = db.session.query(User, Subscription, Plan).join(
            Subscription, User.id == Subscription.user_id, isouter=True
        ).join(
            Plan, User.plan_id == Plan.id, isouter=True
        ).filter(User.user_type == 'user').all()
        
        result = []
        for user, subscription, plan in users:
            usage = Usage.query.filter_by(user_id=user.id).first()
            
            result.append({
                "id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                "plan_id": user.plan_id,
                "plan_name": plan.name if plan else "No Plan",
                "character_limit": plan.character_limit if plan else 0,
                "characters_used": usage.characters_used if usage else 0,
                "characters_remaining": usage.characters_remaining if usage else 0,
                "subscription": {
                    "id": subscription.id if subscription else None,
                    "status": subscription.status if subscription else "inactive",
                    "start_date": subscription.start_date.isoformat() if subscription and subscription.start_date else None,
                    "end_date": subscription.end_date.isoformat() if subscription and subscription.end_date else None,
                    "created_at": subscription.created_at.isoformat() if subscription and subscription.created_at else None
                } if subscription else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            })
            
        return jsonify({"users": result, "total": len(result)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Update subscription status
@admin_bp.route('/subscription/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    try:
        from app.models.subscription import Subscription
        
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return jsonify({"error": "Subscription not found"}), 404
            
        data = request.get_json()
        
        if 'status' in data:
            subscription.status = data['status']
        if 'end_date' in data:
            subscription.end_date = datetime.fromisoformat(data['end_date'])
        if 'start_date' in data:
            subscription.start_date = datetime.fromisoformat(data['start_date'])
            
        subscription.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Subscription updated successfully",
            "subscription": {
                "id": subscription.id,
                "status": subscription.status,
                "start_date": subscription.start_date.isoformat() if subscription.start_date else None,
                "end_date": subscription.end_date.isoformat() if subscription.end_date else None
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500