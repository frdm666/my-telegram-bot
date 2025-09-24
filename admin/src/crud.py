from sqlalchemy.orm import Session
from .models import AllowedUser

def get_users(db: Session):
    return db.query(AllowedUser).all()

def create_user(db: Session, user_id: int, username: str):
    db_user = AllowedUser(user_id=user_id, username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, username: str):
    db_user = db.query(AllowedUser).filter(AllowedUser.user_id == user_id).first()
    if db_user:
        db_user.username = username
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(AllowedUser).filter(AllowedUser.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user