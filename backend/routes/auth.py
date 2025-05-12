from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin):
    """
    Authenticate a user and return an access token.
    This is a placeholder that will be implemented with Supabase authentication.
    """
    # TODO: Implement actual Supabase authentication
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not yet implemented"
    ) 