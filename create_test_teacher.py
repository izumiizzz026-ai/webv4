"""
Script to create a test teacher account for testing the QR scanner.
Run this script to create a teacher account with the following credentials:
Email: testteacher@example.com
Password: test123
"""
import sys
import os

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Teacher, bcrypt

def create_test_teacher():
    with app.app_context():
        # Check if teacher already exists
        existing_teacher = Teacher.query.filter_by(email='testteacher@example.com').first()
        
        if existing_teacher:
            print("Test teacher account already exists!")
            print(f"Email: testteacher@example.com")
            print(f"Password: test123")
            return
        
        # Create new teacher
        hashed_password = bcrypt.generate_password_hash('test123').decode('utf-8')
        
        new_teacher = Teacher(
            full_name='Test Teacher',
            email='testteacher@example.com',
            password_hash=hashed_password
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        
        print("=" * 50)
        print("Test Teacher Account Created Successfully!")
        print("=" * 50)
        print("Email: testteacher@example.com")
        print("Password: test123")
        print("=" * 50)
        print("\nYou can now login at http://localhost:5000/")
        print("Select 'Teacher' option and use the credentials above.")
        print("=" * 50)

if __name__ == '__main__':
    create_test_teacher()

