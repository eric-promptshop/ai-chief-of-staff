"""
Unit tests for the Supabase service.
"""
import pytest
from unittest.mock import patch, MagicMock
from services.supabase import SupabaseService

@pytest.fixture
def mock_supabase_client():
    """Fixture for mocking the Supabase client."""
    with patch('services.supabase.create_client') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance

class TestSupabaseService:
    """Tests for the SupabaseService class."""

    def test_initialization(self, mock_supabase_client):
        """Test that the service initializes correctly."""
        with patch('services.supabase.get_settings') as mock_settings:
            mock_settings.return_value.SUPABASE_URL = 'https://test.supabase.co'
            mock_settings.return_value.SUPABASE_KEY = 'test-key'
            
            service = SupabaseService()
            assert service._client is not None
            mock_supabase_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id(self, mock_supabase_client):
        """Test get_by_id method."""
        # Setup mock response
        mock_execute = MagicMock()
        mock_execute.execute.return_value.data = [{"id": "123", "name": "Test"}]
        mock_supabase_client.from_.return_value.select.return_value.eq.return_value = mock_execute
        
        # Create service instance
        service = SupabaseService()
        
        # Call the method
        result = await service.get_by_id("users", "123")
        
        # Assertions
        assert result == {"id": "123", "name": "Test"}
        mock_supabase_client.from_.assert_called_once_with("users")
        mock_supabase_client.from_.return_value.select.assert_called_once_with("*")
        mock_supabase_client.from_.return_value.select.return_value.eq.assert_called_once_with("id", "123")

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, mock_supabase_client):
        """Test get_by_id method when record is not found."""
        # Setup mock response
        mock_execute = MagicMock()
        mock_execute.execute.return_value.data = []
        mock_supabase_client.from_.return_value.select.return_value.eq.return_value = mock_execute
        
        # Create service instance
        service = SupabaseService()
        
        # Call the method
        result = await service.get_by_id("users", "456")
        
        # Assertions
        assert result is None
        mock_supabase_client.from_.assert_called_once_with("users") 