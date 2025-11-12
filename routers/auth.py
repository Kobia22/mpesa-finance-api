# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from crud.user import get_user_by_email, create_user
from database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse, tags=["Authentication"])
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return create_user(db, user=user_in)

@router.get("/test")
async def auth_test():
    return {"message": "Auth router is working!"}