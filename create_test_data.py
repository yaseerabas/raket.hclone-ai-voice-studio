#!/usr/bin/env python3
# create_test_data.py
from app import create_app, db
from app.models.user import User
from app.models.plan import Plan
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create admin user if not exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            user_type='admin'
        )
        db.session.add(admin)
        print("Admin user created: admin@example.com / admin123")
    
    # Create test user if not exists
    user = User.query.filter_by(email='user@example.com').first()
    if not user:
        user = User(
            email='user@example.com',
            password=generate_password_hash('password123'),
            user_type='user'
        )
        db.session.add(user)
        print("Test user created: user@example.com / password123")
    
    # Create test plans if not exist
    plans_data = [
        {"name": "Basic", "character_limit": 10000},
        {"name": "Pro", "character_limit": 50000},
        {"name": "Premium", "character_limit": 100000}
    ]
    
    for plan_data in plans_data:
        plan = Plan.query.filter_by(name=plan_data['name']).first()
        if not plan:
            plan = Plan(
                name=plan_data['name'],
                character_limit=plan_data['character_limit']
            )
            db.session.add(plan)
            print(f"Plan created: {plan_data['name']} - {plan_data['character_limit']} chars")
    
    db.session.commit()
    print("Test data created successfully!")