# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse
from crud.user import get_user_by_email, create_user, verify_password
from auth.jwt import create_access_token, create_refresh_token
from database import get_db
from auth.dependencies import get_current_active_user, get_current_admin_user
from schemas.user import UserResponse
from models.user import User
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
    refresh_token = create_refresh_token(data={"sub": user.email})

    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.get("/test")
async def auth_test():
    return {"message": "Auth router is working!"}

@router.get("/me", response_model=UserResponse, tags=["Authentication"])
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/admin/users", tags=["Admin"])
def list_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    users = db.query(User).all()
    return users

@router.patch("/admin/users/{user_id}", tags=["Admin"])
def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    db.commit()
    return {"message": f"User {user.email} is now an admin"}