import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from config.db import SessionLocal
from .models import User

load_dotenv()

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Request Schema
# =========================
class AuthRequest(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=4)

# =========================
# Register
# =========================
@auth_router.post("/register")
def register(data: AuthRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=409, detail="Username exists")

    new_user = User(
        username=data.username,
        password=pwd_context.hash(data.password),
        is_admin=False
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {"message": "User created"}

# =========================
# Login
# =========================
@auth_router.post("/login")
def login(data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token = jwt.encode({
        "sub": str(user.id),
        "username": user.username,
        "is_admin": user.is_admin,
        "exp": expire
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "user_id": user.id,
        "is_admin": user.is_admin
    }