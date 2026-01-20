# app/routes/contact_routes.py
from flask import Blueprint, request, jsonify
from app.models.contact_message import ContactMessage
from app.schemas.contact_message_schema import ContactMessageSchema
from app import db

contact_bp = Blueprint('contact', __name__)
contact_schema = ContactMessageSchema()

# Submit Contact Message
@contact_bp.route('/submit', methods=['POST', 'OPTIONS'])
@contact_bp.route('/', methods=['POST', 'OPTIONS'])
def submit_contact():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        errors = contact_schema.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        message = ContactMessage(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({"message": "Contact message submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500