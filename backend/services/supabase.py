"""
Supabase service module for interacting with Supabase.
"""
import logging
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from supabase import create_client, Client
from config.settings import get_settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)
settings = get_settings()

T = TypeVar('T')

class SupabaseService:
    """Service for Supabase database operations."""
    
    def __init__(self):
        """Initialize the Supabase client."""
        self._client = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish connection to Supabase."""
        try:
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Connected to Supabase successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {str(e)}")
            raise
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if not self._client:
            self._connect()
        return self._client
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def query(self, table: str, query_fn=None):
        """
        Execute a query on a table with retry logic.
        
        Args:
            table: The table to query
            query_fn: Function that takes a query and returns a modified query
                      Example: lambda q: q.select('*').eq('status', 'active')
        
        Returns:
            Query result
        """
        try:
            query = self.client.from_(table)
            if query_fn:
                query = query_fn(query)
            result = await query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Supabase query error on table {table}: {str(e)}")
            raise
    
    async def get_by_id(self, table: str, id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID."""
        try:
            result = await self.client.from_(table).select("*").eq("id", id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching {table} with ID {id}: {str(e)}")
            raise
    
    async def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        try:
            result = await self.client.from_(table).insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error creating record in {table}: {str(e)}")
            raise
    
    async def update(self, table: str, id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record by ID."""
        try:
            result = await self.client.from_(table).update(data).eq("id", id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating {table} with ID {id}: {str(e)}")
            raise
    
    async def delete(self, table: str, id: str) -> Dict[str, Any]:
        """Delete a record by ID."""
        try:
            result = await self.client.from_(table).delete().eq("id", id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error deleting {table} with ID {id}: {str(e)}")
            raise
    
    async def get_auth_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information from auth.users table."""
        try:
            result = await self.client.rpc("get_auth_user", {"user_id": user_id}).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching auth user with ID {user_id}: {str(e)}")
            raise

# Create a singleton instance
supabase = SupabaseService() 