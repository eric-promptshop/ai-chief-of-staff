from typing import Optional, List, Dict
from pydantic import Field

from .base import SupabaseModel

class Document(SupabaseModel):
    """Document model for managing user documents and their embeddings."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    user_id: str  # Reference to the user who owns this document
    embedding_id: Optional[str] = None  # Reference to vector embedding in Pinecone
    metadata: Dict = Field(default_factory=dict)  # Additional metadata about the document
    tags: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None  # Original source of the document if applicable
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "title": "Q1 2024 Marketing Strategy",
                "content": "Our marketing strategy for Q1 2024 focuses on...",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "embedding_id": "vec_123456",
                "metadata": {
                    "author": "Marketing Team",
                    "department": "Marketing",
                    "version": "1.0"
                },
                "tags": ["marketing", "strategy", "2024"],
                "source_url": "https://company-drive.com/docs/marketing-strategy.pdf"
            }
        } 