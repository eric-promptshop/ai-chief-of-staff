from fastapi import APIRouter
from supabase import create_client
from config import API_KEYS

supabase = create_client(API_KEYS["supabase_url"], API_KEYS["supabase_key"])
router = APIRouter()

@router.get("/logs/{agent_id}")
def get_logs(agent_id: str):
    response = supabase.table("agent_logs").select("*").eq("agent_id", agent_id).execute()
    return {"agent_id": agent_id, "logs": response.data}