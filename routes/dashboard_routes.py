from fastapi import APIRouter, Depends
from config.database import get_database
from core.auth import require_role
from services.dashboard_service import get_dashboard_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard(db=Depends(get_database), current_user=Depends(require_role(["viewer", "admin", "analyst"]))):
    return await get_dashboard_summary(db)
