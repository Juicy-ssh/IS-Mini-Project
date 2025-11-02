# crud.py
from sqlalchemy.orm import Session
import models, schemas, security

# --- User CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Generate unique username (6 chars min)
    while True:
        username = security.generate_unique_code(6)
        if not get_user_by_username(db, username=username):
            break

    # Generate key (10 chars)
    key = security.generate_unique_code(10)

    # Hash the key as password
    hashed_password = security.get_password_hash(key)

    # Create active user
    db_user = models.User(
        username=username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, key

# --- File CRUD ---
def create_file_record(db: Session, filename: str, saved_filename: str, owner_id: int, recipient_id: int | None = None, uploaded_at=None):
    db_file = models.File(
        filename=filename,
        saved_filename=saved_filename,
        owner_id=owner_id,
        recipient_id=recipient_id,
        uploaded_at=uploaded_at
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file_by_saved_name(db: Session, saved_filename: str):
    return db.query(models.File).filter(models.File.saved_filename == saved_filename).first()

def get_files_by_recipient(db: Session, recipient_id: int):
    return db.query(models.File).filter(models.File.recipient_id == recipient_id).all()

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_all_files(db: Session):
    return db.query(models.File).all()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def delete_file(db: Session, file_id: int):
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False
