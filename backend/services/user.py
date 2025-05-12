"""User service for handling user-related business logic."""

from typing import Optional, Dict
from models.user import User
from repositories.user import UserRepository
from .base import BaseService

class UserService(BaseService[User]):
    """Service for user-related operations."""
    
    def __init__(self):
        """Initialize user service."""
        super().__init__(UserRepository())
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User if found, None otherwise
        """
        return await self.repository.get_by_email(email)
    
    async def update_preferences(self, user_id: str, preferences: Dict) -> Optional[User]:
        """Update user preferences.
        
        Args:
            user_id: User ID
            preferences: New preferences to set or update
            
        Returns:
            Updated user if found, None otherwise
        """
        user = await self.get(user_id)
        if not user:
            return None
            
        # Merge new preferences with existing ones
        updated_preferences = {**user.preferences, **preferences}
        return await self.update(user_id, {"preferences": updated_preferences})
    
    async def create_user(self, email: str, full_name: str, avatar_url: Optional[str] = None) -> User:
        """Create a new user.
        
        Args:
            email: User's email address
            full_name: User's full name
            avatar_url: Optional URL to user's avatar
            
        Returns:
            Created user instance
        """
        user_data = {
            "email": email,
            "full_name": full_name,
            "avatar_url": avatar_url,
            "is_active": True,
            "preferences": {}
        }
        return await self.create(user_data) 