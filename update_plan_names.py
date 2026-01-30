#!/usr/bin/env python3
"""
Update existing plan names and character limits to new values
Run this script to migrate old plan names to new ones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.plan import Plan

def update_plan_names():
    """Update plan names from old to new format"""
    app = create_app()
    
    with app.app_context():
        try:
            # Mapping from old names to new names and character limits
            plan_updates = {
                'Basic': {'new_name': '1M Plan', 'character_limit': 1000000},
                'Pro': {'new_name': '3M Plan', 'character_limit': 3000000},
                'Premium': {'new_name': '5M Plan', 'character_limit': 5000000},
                'Enterprise': {'new_name': '10M Plan', 'character_limit': 10000000},
                # Also handle old names like Low, Middle, High
                'Low': {'new_name': '1M Plan', 'character_limit': 1000000},
                'Middle': {'new_name': '3M Plan', 'character_limit': 3000000},
                'High': {'new_name': '5M Plan', 'character_limit': 5000000},
            }
            
            updated_count = 0
            
            for old_name, update_data in plan_updates.items():
                plan = Plan.query.filter_by(name=old_name).first()
                if plan:
                    print(f"🔄 Updating '{old_name}' to '{update_data['new_name']}' with {update_data['character_limit']:,} characters")
                    plan.name = update_data['new_name']
                    plan.character_limit = update_data['character_limit']
                    updated_count += 1
            
            db.session.commit()
            
            if updated_count > 0:
                print(f"\n✅ Updated {updated_count} plan(s)")
            else:
                print("ℹ️  No old plan names found to update")
            
            # Display all current plans
            print("\n📋 Current Plans:")
            all_plans = Plan.query.all()
            for plan in all_plans:
                user_count = len(plan.subscriptions) if hasattr(plan, 'subscriptions') else 0
                print(f"   - ID: {plan.id}, Name: {plan.name}, Limit: {plan.character_limit:,} characters, Users: {user_count}")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating plans: {e}")
            return False
            
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("Plan Name Migration Script")
    print("=" * 50)
    update_plan_names()
