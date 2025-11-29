# crud.py

from sqlalchemy.orm import Session
import models, schemas

# ---------- CREATE ----------
def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(name=user.name, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------- READ ONE ----------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# ---------- READ ALL ----------
def get_all_users(db: Session):
    return db.query(models.User).all()

# ---------- UPDATE ----------
def update_user(db: Session, user_id: int, data: schemas.UserCreate):
    user = get_user(db, user_id)
    if not user:
        return None

    user.name = data.name
    user.age = data.age

    db.commit()
    db.refresh(user)
    return user

# ---------- DELETE ----------
def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user

from auth import hash_password, verify_password

# SIGNUP
def create_user_auth(db: Session, user: schemas.UserSignup):
    hashed_pw = hash_password(user.password)

    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# LOGIN
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
