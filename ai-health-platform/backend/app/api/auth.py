"""
Authentication API endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.database import get_db
from app.models.user import User

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    age: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    age: Optional[int]
    is_onboarded: bool
    
    class Config:
        from_attributes = True





# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)





def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()





# Endpoints
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user (no authentication)"""
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        age=user_data.age
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user









