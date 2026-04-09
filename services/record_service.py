from bson import ObjectId
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
from models.record import create_record_doc, doc_to_record_res
from schemas.record import RecordCreate, RecordUpdate

async def create_record(db, record_in: RecordCreate, user_id: str):
    record_doc = create_record_doc(record_in.model_dump(), user_id)
    result = await db["financial_records"].insert_one(record_doc)
    record_doc["_id"] = result.inserted_id
    return doc_to_record_res(record_doc)

async def get_records(db,
                      type_filter: Optional[str] = None,
                      category: Optional[str] = None,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None):
    query = {}
    if type_filter:
        query["type"] = type_filter
    if category:
        query["category"] = category
    if start_date or end_date:
        query["date"] = {}
        if start_date:
            query["date"]["$gte"] = start_date
        if end_date:
            query["date"]["$lte"] = end_date
            
    cursor = db["financial_records"].find(query).sort("date", -1)
    records = await cursor.to_list(length=100)
    return [doc_to_record_res(record) for record in records]

async def update_record(db, record_id: str, record_in: RecordUpdate):
    update_data = {k: v for k, v in record_in.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
        
    result = await db["financial_records"].update_one(
        {"_id": ObjectId(record_id)}, {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        
    doc = await db["financial_records"].find_one({"_id": ObjectId(record_id)})
    return doc_to_record_res(doc)

async def delete_record(db, record_id: str):
    result = await db["financial_records"].delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"message": "Record deleted successfully"}
