from typing import Optional, List, Dict
from datetime import datetime
from pydantic import Field

from .base import SupabaseModel

class Message(SupabaseModel):
    """Individual message in a conversation."""
    content: str = Field(..., min_length=1)
    role: str = Field(..., pattern="^(user|assistant|system)$")  # Matches OpenAI chat roles
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict = Field(default_factory=dict)  # Additional message metadata

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "content": "Can you help me analyze this quarterly report?",
                "role": "user",
                "timestamp": "2024-03-20T10:30:00Z",
                "metadata": {
                    "document_references": ["doc_123", "doc_456"],
                    "confidence_score": 0.95
                }
            }
        }

class Conversation(SupabaseModel):
    """Conversation model for managing chat interactions."""
    user_id: str  # Reference to the user who owns this conversation
    title: str = Field(..., min_length=1, max_length=200)
    messages: List[Message] = Field(default_factory=list)
    context: Dict = Field(default_factory=dict)  # Conversation context and settings
    is_active: bool = True
    last_interaction: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Quarterly Report Analysis",
                "messages": [
                    {
                        "content": "Can you help me analyze this quarterly report?",
                        "role": "user",
                        "timestamp": "2024-03-20T10:30:00Z",
                        "metadata": {
                            "document_references": ["doc_123", "doc_456"],
                            "confidence_score": 0.95
                        }
                    }
                ],
                "context": {
                    "relevant_documents": ["Q1_2024_Report.pdf"],
                    "analysis_focus": "revenue trends",
                    "preferred_style": "detailed"
                },
                "is_active": True,
                "last_interaction": "2024-03-20T10:30:00Z"
            }
        } 