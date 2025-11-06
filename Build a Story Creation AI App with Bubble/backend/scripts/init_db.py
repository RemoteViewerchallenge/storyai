#!/usr/bin/env python3
"""
Database initialization script for Story AI Backend
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.db import db
from src.models.user import User
from src.models.character import Character, Story, StorySegment
from src.models.subscription import *

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Print table information
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {', '.join(tables)}")

def reset_database():
    """Reset the database (drop and recreate all tables)"""
    with app.app_context():
        print("Dropping all database tables...")
        db.drop_all()
        print("Creating fresh database tables...")
        db.create_all()
        print("Database reset successfully!")

def create_sample_data():
    """Create sample data for testing"""
    with app.app_context():
        # Check if sample data already exists
        if Character.query.first():
            print("Sample data already exists. Skipping...")
            return
        
        print("Creating sample data...")
        
        # Create sample character
        sample_character = Character(
            user_id="sample_user_123",
            name="Sample Hero",
            perspective="1st_person",
            gender="male",
            variant="male_1",
            career="ceo",
            image_style="anime"
        )
        
        # Set sample traits
        sample_traits = {
            'personality': ['ambitious', 'decisive', 'strategic', 'confident'],
            'background': 'A successful male executive with years of corporate experience.',
            'goals': ['expand business empire', 'maintain work-life balance', 'mentor others']
        }
        sample_character.set_traits_dict(sample_traits)
        
        db.session.add(sample_character)
        db.session.commit()
        
        print(f"Created sample character with ID: {sample_character.id}")
        print("Sample data created successfully!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management for Story AI Backend')
    parser.add_argument('action', choices=['init', 'reset', 'sample'], 
                       help='Action to perform: init (create tables), reset (drop and recreate), sample (add sample data)')
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_database()
    elif args.action == 'reset':
        reset_database()
    elif args.action == 'sample':
        create_sample_data()

