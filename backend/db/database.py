from typing import Optional, Dict, Any
from supabase import create_client, Client

from config.settings import settings

class Database:
    """Database connection and operations manager."""
    _instance: Optional['Database'] = None
    _client: Optional[Client] = None

    def __new__(cls) -> 'Database':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize database connection if not already initialized."""
        if Database._client is None:
            Database._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )

    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if self._client is None:
            raise RuntimeError("Database client not initialized")
        return self._client

    async def execute(self, table: str, query_type: str, data: Dict[str, Any] = None, **kwargs) -> Dict:
        """Execute a database operation.
        
        Args:
            table: Name of the table to operate on
            query_type: Type of query ('select', 'insert', 'update', 'delete', 'upsert')
            data: Data for insert/update operations
            **kwargs: Additional query parameters
        
        Returns:
            Query result
        """
        query = self.client.table(table)

        if query_type == 'select':
            # Handle select query parameters
            if kwargs.get('columns'):
                query = query.select(kwargs['columns'])
            if kwargs.get('filters'):
                for filter_dict in kwargs['filters']:
                    query = query.filter(
                        filter_dict['column'],
                        filter_dict['operator'],
                        filter_dict['value']
                    )
            if kwargs.get('order_by'):
                query = query.order(kwargs['order_by'])
            if kwargs.get('limit'):
                query = query.limit(kwargs['limit'])
            
            result = await query.execute()
            return result.data

        elif query_type == 'insert':
            result = await query.insert(data).execute()
            return result.data

        elif query_type == 'update':
            if not kwargs.get('match_column'):
                raise ValueError("match_column is required for update operations")
            
            result = await query.update(data).match(
                {kwargs['match_column']: kwargs['match_value']}
            ).execute()
            return result.data

        elif query_type == 'upsert':
            result = await query.upsert(data).execute()
            return result.data

        elif query_type == 'delete':
            if not kwargs.get('match_column'):
                raise ValueError("match_column is required for delete operations")
            
            result = await query.delete().match(
                {kwargs['match_column']: kwargs['match_value']}
            ).execute()
            return result.data

        else:
            raise ValueError(f"Unsupported query type: {query_type}")

# Create a global database instance
db = Database() 