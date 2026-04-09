from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from datetime import datetime
from schemas.record import RecordCreate, RecordResponse, RecordUpdate, CategoryType
from config.database import get_database
from core.auth import require_role
from services.record_service import create_record, get_records, update_record, delete_record

router = APIRouter(prefix="/records", tags=["records"])

@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_new_record(record_in: RecordCreate, db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await create_record(db, record_in, str(current_user["_id"]))

@router.get("/", response_model=List[RecordResponse])
async def list_records(
    type: Optional[str] = Query(None, pattern="^(income|expense)$"),
    category: Optional[CategoryType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db=Depends(get_database),
    current_user=Depends(require_role(["admin", "analyst"]))
):
    return await get_records(db, type, category, start_date, end_date)

@router.patch("/{record_id}", response_model=RecordResponse)
async def update_existing_record(record_id: str, record_in: RecordUpdate, db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await update_record(db, record_id, record_in)

@router.delete("/{record_id}")
async def delete_existing_record(record_id: str, db=Depends(get_database), current_user=Depends(require_role(["admin"]))):
    return await delete_record(db, record_id)
