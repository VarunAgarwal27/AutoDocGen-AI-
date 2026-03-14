from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register Route

@router.post("/register")
def register_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully ✅"}

# Login Route

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Current Active User

@router.get("/me")
def get_current_user(authorization: str = Header(...)):
    """
    Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    email = decode_access_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return {"email": email}
