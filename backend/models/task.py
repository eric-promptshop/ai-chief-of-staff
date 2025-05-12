from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field

from .base import SupabaseModel

class TaskStatus(str, Enum):
    """Enum for task status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    """Enum for task priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(SupabaseModel):
    """Task model for managing user tasks."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = None
    user_id: str  # Reference to the user who owns this task
    assigned_to: Optional[str] = None  # Optional reference to user assigned to task
    tags: List[str] = Field(default_factory=list)
    completion_date: Optional[datetime] = None
    
    def mark_completed(self):
        """Mark the task as completed and set completion date."""
        self.status = TaskStatus.COMPLETED
        self.completion_date = datetime.utcnow()
        self.update_timestamp()
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Write and review Q2 project proposal",
                "status": "pending",
                "priority": "high",
                "due_date": "2024-04-15T00:00:00Z",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "assigned_to": "123e4567-e89b-12d3-a456-426614174001",
                "tags": ["project", "documentation"],
                "completion_date": None
            }
        } 