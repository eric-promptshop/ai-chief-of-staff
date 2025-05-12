from typing import List, Optional, Dict
from models.document import Document
from .base import BaseRepository

class DocumentRepository(BaseRepository[Document]):
    """Repository for document operations."""
    
    def __init__(self):
        """Initialize document repository."""
        super().__init__(Document, 'documents')
    
    async def get_user_documents(
        self, 
        user_id: str,
        tags: Optional[List[str]] = None
    ) -> List[Document]:
        """Get documents for a specific user.
        
        Args:
            user_id: User ID
            tags: Optional list of tags to filter by
            
        Returns:
            List of documents matching the criteria
        """
        filters = [{'column': 'user_id', 'operator': 'eq', 'value': user_id}]
        
        if tags:
            # Supabase array contains operator
            filters.append({'column': 'tags', 'operator': 'cs', 'value': tags})
            
        return await self.filter(filters=filters)
    
    async def update_embedding(
        self,
        document_id: str,
        embedding_id: str,
        metadata: Optional[Dict] = None
    ) -> Optional[Document]:
        """Update document's embedding ID and metadata.
        
        Args:
            document_id: Document ID
            embedding_id: Pinecone vector ID
            metadata: Optional additional metadata
            
        Returns:
            Updated document if found, None otherwise
        """
        update_data = {'embedding_id': embedding_id}
        
        if metadata:
            update_data['metadata'] = metadata
            
        return await self.update(document_id, update_data) 