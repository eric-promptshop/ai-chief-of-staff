from typing import Optional
from pydantic import EmailStr, Field

from .base import SupabaseModel

class User(SupabaseModel):
    """User model for authentication and profile information."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True
    avatar_url: Optional[str] = None
    preferences: dict = Field(default_factory=dict)  # Store user preferences as JSON
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "avatar_url": "https://example.com/avatar.jpg",
                "preferences": {
                    "theme": "light",
                    "notifications_enabled": True
                }
            }
        } 