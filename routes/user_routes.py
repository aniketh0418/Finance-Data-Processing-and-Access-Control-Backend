from fastapi import APIRouter, Depends, status
from typing import List
from schemas.user import UserCreate, UserResponse, UserUpdateRole, UserUpdateStatus
from config.database import get_database
from core.auth import require_role
from services.user_service import register_user, get_all_users, update_user_role, set_user_status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db=Depends(get_database)):
    return await register_user(db, user_in)

@router.get("/", response_model=List[UserResponse])
async def list_users(db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await get_all_users(db)

@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_role(user_id: str, payload: UserUpdateRole, db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await update_user_role(db, user_id, payload)

@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_status(user_id: str, payload: UserUpdateStatus, db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await set_user_status(db, user_id, payload)
