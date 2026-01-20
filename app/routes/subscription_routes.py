# app/routes/subscription_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.schemas.plan_schema import PlanSchema
from app.schemas.subscription_schema import SubscriptionSchema
from app import db
from datetime import datetime, timedelta

subscription_bp = Blueprint('subscription', __name__)
plan_schema = PlanSchema()
subscription_schema = SubscriptionSchema()

# app/routes/subscription_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.models.usage import Usage
from app.schemas.plan_schema import PlanSchema
from app.schemas.subscription_schema import SubscriptionSchema
from app import db
from datetime import datetime, timedelta

subscription_bp = Blueprint('subscription', __name__)
plan_schema = PlanSchema()
subscription_schema = SubscriptionSchema()

# Get all plans (no auth required for viewing plans)
@subscription_bp.route('/plans', methods=['GET'])
def get_plans():
    try:
        plans = Plan.query.all()
        result = []
        for plan in plans:
            result.append({
                "id": plan.id,
                "name": plan.name,
                "character_limit": plan.character_limit,
                "created_at": plan.created_at.isoformat() if plan.created_at else None
            })
        return jsonify({"plans": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Create subscription
@subscription_bp.route('/create', methods=['POST'])
@jwt_required()
def create_subscription():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        plan_id = data.get('plan_id')
        if not plan_id:
            return jsonify({"error": "plan_id is required"}), 400
            
        # Check if user exists
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if plan exists
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({"error": "Plan not found"}), 404

        # Check if user already has active subscription
        existing = Subscription.query.filter_by(user_id=int(user_id), status='active').first()
        if existing:
            # Update existing subscription instead of creating new
            existing.plan_id = plan_id
            existing.updated_at = datetime.utcnow()
            subscription = existing
        else:
            # Create new subscription
            subscription = Subscription(
                user_id=int(user_id), 
                plan_id=plan_id,
                status='active'
            )
            db.session.add(subscription)
            
        # Update user's plan
        user.plan_id = plan_id
        user.updated_at = datetime.utcnow()
        
        # Update or create usage
        usage = Usage.query.filter_by(user_id=int(user_id)).first()
        if usage:
            usage.characters_remaining = plan.character_limit
            usage.characters_used = 0
        else:
            usage = Usage(
                user_id=int(user_id),
                characters_remaining=plan.character_limit,
                characters_used=0
            )
            db.session.add(usage)
            
        db.session.commit()
        
        return jsonify({
            "message": "Subscription created successfully",
            "subscription_id": subscription.id,
            "plan_name": plan.name,
            "character_limit": plan.character_limit,
            "status": subscription.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get user subscription
@subscription_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_subscription(user_id):
    try:
        current_user_id = get_jwt_identity()
        if int(current_user_id) != user_id:
            return jsonify({"error": "Access denied"}), 403

        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            return jsonify({"error": "No active subscription"}), 404
            
        result = {
            "id": subscription.id,
            "user_id": subscription.user_id,
            "plan_id": subscription.plan_id,
            "plan_name": subscription.plan.name if subscription.plan else None,
            "character_limit": subscription.plan.character_limit if subscription.plan else 0,
            "status": subscription.status,
            "start_date": subscription.start_date.isoformat() if subscription.start_date else None,
            "end_date": subscription.end_date.isoformat() if subscription.end_date else None,
            "created_at": subscription.created_at.isoformat() if subscription.created_at else None
        }
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get current user subscription
@subscription_bp.route('/my-subscription', methods=['GET'])
@jwt_required()
def get_my_subscription():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Get subscription info
        subscription = Subscription.query.filter_by(user_id=int(user_id), status='active').first()
        
        # Get usage info
        usage = Usage.query.filter_by(user_id=int(user_id)).first()
        
        result = {
            "user_id": user.id,
            "email": user.email,
            "plan_id": user.plan_id,
            "plan_name": user.plan.name if user.plan else None,
            "subscription": {
                "id": subscription.id if subscription else None,
                "status": subscription.status if subscription else "inactive",
                "start_date": subscription.start_date.isoformat() if subscription and subscription.start_date else None
            } if subscription else None,
            "usage": {
                "characters_used": usage.characters_used if usage else 0,
                "characters_remaining": usage.characters_remaining if usage else 0,
                "character_limit": user.plan.character_limit if user.plan else 0
            } if usage else None
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Cancel subscription
@subscription_bp.route('/cancel', methods=['POST'])
@jwt_required()
def cancel_subscription():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        subscription_id = data.get('subscription_id') if data else None
        
        # If no subscription_id provided, cancel current active subscription
        if not subscription_id:
            subscription = Subscription.query.filter_by(user_id=int(user_id), status='active').first()
        else:
            subscription = Subscription.query.get(subscription_id)
            
        if not subscription:
            return jsonify({"error": "No active subscription found"}), 404
            
        if subscription.user_id != int(user_id):
            return jsonify({"error": "Access denied"}), 403

        subscription.status = 'cancelled'
        subscription.updated_at = datetime.utcnow()
        
        # Also update user's plan_id to None
        user = User.query.get(int(user_id))
        if user:
            user.plan_id = None
            user.updated_at = datetime.utcnow()
            
        db.session.commit()
        
        return jsonify({
            "message": "Subscription cancelled successfully",
            "subscription_id": subscription.id,
            "status": subscription.status
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500