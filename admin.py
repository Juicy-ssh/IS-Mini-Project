#!/usr/bin/env python3
"""
Admin management utility for the Secure File Chat Application.

This script provides command-line tools to manage admin users in the database.
"""

import sys
import argparse
from database import SessionLocal
from models import User
import crud
import security
from schemas import UserCreate

def set_admin(username: str):
    """
    Set a user as admin by username.
    """
    db = SessionLocal()
    try:
        user = crud.get_user_by_username(db, username=username)
        if not user:
            print(f"Error: User '{username}' not found.")
            return False

        if user.is_admin:
            print(f"User '{username}' is already an admin.")
            return True

        user.is_admin = True
        db.commit()
        print(f"Successfully set '{username}' as admin.")
        return True
    except Exception as e:
        print(f"Error setting admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def remove_admin(username: str):
    """
    Remove admin privileges from a user by username.
    """
    db = SessionLocal()
    try:
        user = crud.get_user_by_username(db, username=username)
        if not user:
            print(f"Error: User '{username}' not found.")
            return False

        if not user.is_admin:
            print(f"User '{username}' is not an admin.")
            return True

        user.is_admin = False
        db.commit()
        print(f"Successfully removed admin privileges from '{username}'.")
        return True
    except Exception as e:
        print(f"Error removing admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def list_admins():
    """
    List all admin users.
    """
    db = SessionLocal()
    try:
        admins = db.query(User).filter(User.is_admin == True).all()
        if not admins:
            print("No admin users found.")
            return

        print("Admin Users:")
        print("-" * 50)
        for admin in admins:
            print(f"ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")
    except Exception as e:
        print(f"Error listing admins: {e}")
    finally:
        db.close()

def create_admin_user(email: str, password: str = None):
    """
    Create a new admin user.
    If password is not provided, a random key will be generated.
    """
    db = SessionLocal()
    try:
        # Check if email already exists
        existing_user = crud.get_user_by_email(db, email=email)
        if existing_user:
            print(f"Error: Email '{email}' is already registered.")
            return False

        # Create user
        user_data = UserCreate(email=email)
        new_user, key = crud.create_user(db=db, user=user_data)

        # Set as admin
        new_user.is_admin = True
        db.commit()

        actual_password = password if password else key
        if password:
            # Hash the provided password
            new_user.hashed_password = security.get_password_hash(password)
            db.commit()

        print("New admin user created successfully!")
        print(f"Username: {new_user.username}")
        print(f"Email: {new_user.email}")
        print(f"Password/Key: {actual_password}")
        return True
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    parser = argparse.ArgumentParser(description="Admin management utility")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Set admin command
    set_parser = subparsers.add_parser("set-admin", help="Set a user as admin")
    set_parser.add_argument("username", help="Username to set as admin")

    # Remove admin command
    remove_parser = subparsers.add_parser("remove-admin", help="Remove admin privileges from a user")
    remove_parser.add_argument("username", help="Username to remove admin privileges from")

    # List admins command
    subparsers.add_parser("list-admins", help="List all admin users")

    # Create admin command
    create_parser = subparsers.add_parser("create-admin", help="Create a new admin user")
    create_parser.add_argument("email", help="Email address for the new admin user")
    create_parser.add_argument("--password", help="Password for the new admin user (optional, random key will be generated if not provided)")

    args = parser.parse_args()

    if args.command == "set-admin":
        success = set_admin(args.username)
        sys.exit(0 if success else 1)
    elif args.command == "remove-admin":
        success = remove_admin(args.username)
        sys.exit(0 if success else 1)
    elif args.command == "list-admins":
        list_admins()
    elif args.command == "create-admin":
        success = create_admin_user(args.email, args.password)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
