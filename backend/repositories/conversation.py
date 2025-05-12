from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.conversation import Conversation, Message
from .base import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    """Repository for conversation operations."""
    
    def __init__(self):
        """Initialize conversation repository."""
        super().__init__(Conversation, 'conversations')
    
    async def get_user_conversations(
        self,
        user_id: str,
        since: Optional[datetime] = None,
        limit: int = 50
    ) -> List[Conversation]:
        """Get conversations for a specific user.
        
        Args:
            user_id: User ID
            since: Optional datetime to filter conversations from
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversations matching the criteria
        """
        filters = [{'column': 'user_id', 'operator': 'eq', 'value': user_id}]
        
        if since:
            filters.append({
                'column': 'updated_at',
                'operator': 'gte',
                'value': since.isoformat()
            })
            
        return await self.filter(
            filters=filters,
            order_by=[{'column': 'updated_at', 'order': 'desc'}],
            limit=limit
        )
    
    async def add_message(
        self,
        conversation_id: str,
        message: Message
    ) -> Optional[Conversation]:
        """Add a new message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            message: Message to add
            
        Returns:
            Updated conversation if found, None otherwise
        """
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
            
        conversation.messages.append(message)
        conversation.update_timestamp()
        
        return await self.update(
            conversation_id,
            {
                'messages': [msg.dict() for msg in conversation.messages],
                'updated_at': conversation.updated_at
            }
        ) 