from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    assigned_agent_id: Optional[str] = None

@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    """
    Create a new task.
    This is a placeholder that will be implemented with Supabase database.
    """
    # TODO: Implement actual task creation in Supabase
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Task creation not yet implemented"
    )

@router.get("/", response_model=List[Task])
async def list_tasks():
    """
    List all tasks.
    This is a placeholder that will be implemented with Supabase database.
    """
    # TODO: Implement actual task listing from Supabase
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Task listing not yet implemented"
    ) 