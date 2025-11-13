# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from crud.user import get_user_by_email, create_user, verify_password
from auth.jwt import create_access_token
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

@router.post("/login",tags=["Authentication"])
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
@router.get("/test")
async def auth_test():
    return {"message": "Auth router is working!"}