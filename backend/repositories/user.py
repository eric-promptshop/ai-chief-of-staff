from typing import Optional
from models.user import User
from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for user operations."""
    
    def __init__(self):
        """Initialize user repository."""
        super().__init__(User, 'users')
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email.
        
        Args:
            email: User's email address
            
        Returns:
            User if found, None otherwise
        """
        result = await self.filter(
            filters=[{'column': 'email', 'operator': 'eq', 'value': email}],
            limit=1
        )
        return result[0] if result else None
    
    async def update_preferences(self, user_id: str, preferences: dict) -> Optional[User]:
        """Update user preferences.
        
        Args:
            user_id: User ID
            preferences: New preferences dictionary
            
        Returns:
            Updated user if found, None otherwise
        """
        return await self.update(user_id, {'preferences': preferences}) 