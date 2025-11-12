# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import uvicorn

# Import routers (will be created soon)
from routers import auth

# Initialize FastAPI app
app = FastAPI(
    title="M-Pesa Finance API",
    description="AI-Ready Personal Finance Backend with Role-Based Auth",
    version="1.0.0",
    contact={
        "name": "Eli Wahome Kobia",
        "email": "kobiaeli04@gmail.com",
        "github": "https://github.com/Kobia22"
    }
)

# CORS Middleware (for Streamlit/React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to M-Pesa Finance API",
        "developer": "Eli Wahome Kobia",
        "status": "Day 1 - Backend Live"
    }

# Health check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "mpesa-finance-api"}

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# === DEV: Create Tables ===
from database import engine
from models import user #imports the user model

user.User.metadata.create_all(bind=engine)