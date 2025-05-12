from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import register_user, authenticate_user, logout_user, get_current_user_from_token
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])

SESSION_COOKIE_NAME = "session_token"
SESSION_COOKIE_PATH = "/"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SAMESITE = "lax"

# Register
@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await register_user(db, user.email, user.password, user.full_name)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

# Login
@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    auth_user = await authenticate_user(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=auth_user.session_token,
        httponly=SESSION_COOKIE_HTTPONLY,
        samesite=SESSION_COOKIE_SAMESITE,
        secure=SESSION_COOKIE_SECURE,
        path=SESSION_COOKIE_PATH
    )
    return auth_user

# Logout
@router.post("/logout")
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db), session_token: Optional[str] = Cookie(None, alias=SESSION_COOKIE_NAME)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(User).where(User.session_token == session_token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")
    await logout_user(db, user)
    response.delete_cookie(SESSION_COOKIE_NAME, path=SESSION_COOKIE_PATH)
    return {"message": "Logged out"}

# Get current user
@router.get("/me", response_model=UserResponse)
async def get_me(db: AsyncSession = Depends(get_db), session_token: Optional[str] = Cookie(None, alias=SESSION_COOKIE_NAME)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    result = await db.execute(select(User).where(User.session_token == session_token))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user 