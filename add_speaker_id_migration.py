"""
Migration script to add speaker_id column to cloned_voices table
Run this once to update your existing database
"""

import pymysql
import os

# Database configuration (update if needed)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # Update if you have a password
DB_NAME = 'tts_saas'

# Connect to database
try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    print(f"Connected to database: {DB_NAME}")
    
    with connection.cursor() as cursor:
        # Check if column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = %s 
            AND table_name = 'cloned_voices' 
            AND column_name = 'speaker_id'
        """, (DB_NAME,))
        
        result = cursor.fetchone()
        
        if result is None:
            print("Adding speaker_id column...")
            # Add the speaker_id column
            cursor.execute("""
                ALTER TABLE cloned_voices 
                ADD COLUMN speaker_id VARCHAR(100) NULL
            """)
            connection.commit()
            print("✓ Successfully added speaker_id column to cloned_voices table")
        else:
            print("✓ speaker_id column already exists")
            
except pymysql.Error as e:
    print(f"✗ Database error: {str(e)}")
except Exception as e:
    print(f"✗ Error during migration: {str(e)}")
finally:
    if 'connection' in locals():
        connection.close()
        print("Database connection closed")
