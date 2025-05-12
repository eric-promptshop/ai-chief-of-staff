"""Base service class with common functionality."""

from typing import TypeVar, Generic, Optional, List, Dict, Any
from pydantic import BaseModel

from repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseService(Generic[ModelType]):
    """Base service with common business logic operations."""
    
    def __init__(self, repository: BaseRepository):
        """Initialize service with repository.
        
        Args:
            repository: Repository instance for database operations
        """
        self.repository = repository
    
    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Create a new record.
        
        Args:
            data: Data to create record with
            
        Returns:
            Created model instance
        """
        return await self.repository.create(data)
    
    async def get(self, id: str) -> Optional[ModelType]:
        """Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance if found, None otherwise
        """
        return await self.repository.get(id)
    
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        """Update a record.
        
        Args:
            id: Record ID
            data: Data to update record with
            
        Returns:
            Updated model instance if found, None otherwise
        """
        return await self.repository.update(id, data)
    
    async def delete(self, id: str) -> bool:
        """Delete a record.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        return await self.repository.delete(id)
    
    async def list(self, filters: Optional[List[Dict[str, Any]]] = None) -> List[ModelType]:
        """List records with optional filters.
        
        Args:
            filters: Optional list of filters to apply
            
        Returns:
            List of model instances
        """
        return await self.repository.list(filters) 