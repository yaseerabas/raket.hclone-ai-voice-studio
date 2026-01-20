#!/usr/bin/env python3
"""
Initialize default plans for the system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.plan import Plan

def create_default_plans():
    """Create 4 default plans"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            # Default plans data
            default_plans = [
                {"name": "Basic", "character_limit": 10000},
                {"name": "Pro", "character_limit": 50000},
                {"name": "Premium", "character_limit": 100000},
                {"name": "Enterprise", "character_limit": 500000}
            ]
            
            created_plans = []
            
            for plan_data in default_plans:
                # Check if plan already exists
                existing_plan = Plan.query.filter_by(name=plan_data['name']).first()
                
                if existing_plan:
                    print(f"✅ Plan '{plan_data['name']}' already exists")
                    continue
                
                # Create new plan
                plan = Plan(
                    name=plan_data['name'],
                    character_limit=plan_data['character_limit']
                )
                
                db.session.add(plan)
                created_plans.append(plan_data['name'])
            
            db.session.commit()
            
            if created_plans:
                print(f"✅ Created {len(created_plans)} new plans:")
                for plan_name in created_plans:
                    print(f"   - {plan_name}")
            else:
                print("ℹ️  All default plans already exist")
            
            # Display all plans
            print("\n📋 Current Plans:")
            all_plans = Plan.query.all()
            for plan in all_plans:
                print(f"   {plan.id}. {plan.name} - {plan.character_limit:,} characters")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating plans: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("🚀 Initializing default plans...\n")
    
    if create_default_plans():
        print("\n🎉 Plans initialization complete!")
    else:
        print("\n❌ Plans initialization failed!")
        sys.exit(1)