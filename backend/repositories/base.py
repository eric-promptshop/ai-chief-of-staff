from typing import TypeVar, Generic, List, Optional, Dict, Any
from pydantic import BaseModel

from db.database import db

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""
    
    def __init__(self, model: type[ModelType], table_name: str):
        """Initialize repository with model class and table name.
        
        Args:
            model: Pydantic model class
            table_name: Name of the database table
        """
        self.model = model
        self.table_name = table_name

    async def create(self, data: Dict[str, Any]) -> ModelType:
        """Create a new record.
        
        Args:
            data: Data to insert
            
        Returns:
            Created model instance
        """
        result = await db.execute(self.table_name, 'insert', data)
        return self.model(**result[0])

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance if found, None otherwise
        """
        result = await db.execute(
            self.table_name,
            'select',
            filters=[{'column': 'id', 'operator': 'eq', 'value': id}]
        )
        return self.model(**result[0]) if result else None

    async def get_all(self, limit: int = 100) -> List[ModelType]:
        """Get all records with optional limit.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        result = await db.execute(
            self.table_name,
            'select',
            limit=limit
        )
        return [self.model(**item) for item in result]

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
        """Update a record by ID.
        
        Args:
            id: Record ID
            data: Data to update
            
        Returns:
            Updated model instance if found, None otherwise
        """
        result = await db.execute(
            self.table_name,
            'update',
            data=data,
            match_column='id',
            match_value=id
        )
        return self.model(**result[0]) if result else None

    async def delete(self, id: str) -> bool:
        """Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        result = await db.execute(
            self.table_name,
            'delete',
            match_column='id',
            match_value=id
        )
        return bool(result)

    async def filter(
        self,
        filters: List[Dict[str, Any]],
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[ModelType]:
        """Get records matching filters.
        
        Args:
            filters: List of filter dictionaries
            order_by: Column to order by
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        result = await db.execute(
            self.table_name,
            'select',
            filters=filters,
            order_by=order_by,
            limit=limit
        )
        return [self.model(**item) for item in result] 