from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from database import engine, SessionLocal, Base

app = FastAPI()

# 1. create tables
Base.metadata.create_all(bind=engine)

# 2. DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. ROUTES

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[schemas.UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

from jwt_handler import create_access_token

# SIGNUP
@app.post("/auth/signup")
def signup(user: schemas.UserSignup, db: Session = Depends(get_db)):
    # check if user exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = crud.create_user_auth(db, user)
    return {"message": "User created successfully", "id": created_user.id}

# LOGIN
@app.post("/auth/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(db, user.email, user.password)

    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate JWT
    token = create_access_token({"user_id": authenticated_user.id})

    return {"access_token": token, "token_type": "bearer"}

from fastapi import Header

@app.get("/profile")
def profile(token: str = Header(...), db: Session = Depends(get_db)):
    try:
        from jose import jwt
        payload = jwt.decode(token, "SUPERSECRETJWTKEY", algorithms=["HS256"])
        user_id = payload.get("user_id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user
