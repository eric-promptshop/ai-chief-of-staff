from typing import List, Optional
from datetime import datetime
from models.task import Task, TaskStatus
from .base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """Repository for task operations."""
    
    def __init__(self):
        """Initialize task repository."""
        super().__init__(Task, 'tasks')
    
    async def get_user_tasks(
        self, 
        user_id: str, 
        status: Optional[TaskStatus] = None,
        due_before: Optional[datetime] = None
    ) -> List[Task]:
        """Get tasks for a specific user.
        
        Args:
            user_id: User ID
            status: Optional status filter
            due_before: Optional due date filter
            
        Returns:
            List of tasks matching the criteria
        """
        filters = [{'column': 'user_id', 'operator': 'eq', 'value': user_id}]
        
        if status:
            filters.append({'column': 'status', 'operator': 'eq', 'value': status})
        
        if due_before:
            filters.append({'column': 'due_date', 'operator': 'lte', 'value': due_before.isoformat()})
            
        return await self.filter(filters=filters)
    
    async def mark_completed(self, task_id: str) -> Optional[Task]:
        """Mark a task as completed.
        
        Args:
            task_id: Task ID
            
        Returns:
            Updated task if found, None otherwise
        """
        return await self.update(task_id, {
            'status': TaskStatus.COMPLETED,
            'completed_at': datetime.utcnow()
        }) 