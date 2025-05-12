from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class TimestampedModel(BaseModel):
    """Base model with created_at and updated_at timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    def update_timestamp(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

class SupabaseModel(TimestampedModel):
    """Base model for Supabase tables with ID."""
    id: Optional[str] = None  # Supabase uses UUID strings for IDs 