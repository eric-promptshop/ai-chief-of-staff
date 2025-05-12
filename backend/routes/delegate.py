from fastapi import APIRouter
from supabase import create_client
from config import API_KEYS

supabase = create_client(API_KEYS["supabase_url"], API_KEYS["supabase_key"])
router = APIRouter()

@router.post("/delegate")
def delegate_task(task: str):
    supabase.table("delegated_tasks").insert({"task": task}).execute()
    return {"status": "delegated", "task": task}