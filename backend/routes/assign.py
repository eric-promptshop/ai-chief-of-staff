from fastapi import APIRouter
from supabase import create_client
from config import API_KEYS

supabase = create_client(API_KEYS["supabase_url"], API_KEYS["supabase_key"])
router = APIRouter()

@router.post("/assign")
def assign_agent(agent_name: str, task: str):
    supabase.table("assigned_tasks").insert({"agent": agent_name, "task": task}).execute()
    return {"status": "assigned", "agent": agent_name, "task": task}