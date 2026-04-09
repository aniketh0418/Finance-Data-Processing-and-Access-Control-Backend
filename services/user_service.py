from bson import ObjectId
from fastapi import HTTPException, status
from core.security import get_password_hash
from models.user import create_user_doc, doc_to_user_res
from schemas.user import UserCreate, UserUpdateRole, UserUpdateStatus

async def register_user(db, user_in: UserCreate):
    existing = await db["users"].find_one({"email": user_in.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(user_in.password)
    user_doc = create_user_doc(
        name=user_in.name,
        email=user_in.email,
        password_hash=hashed_password,
        role="viewer" # Default role
    )
    result = await db["users"].insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return doc_to_user_res(user_doc)

async def get_all_users(db):
    cursor = db["users"].find({})
    users = await cursor.to_list(length=100)
    return [doc_to_user_res(user) for user in users]

async def update_user_role(db, user_id: str, payload: UserUpdateRole):
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"role": payload.role}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or role unchanged")
    doc = await db["users"].find_one({"_id": ObjectId(user_id)})
    return doc_to_user_res(doc)

async def set_user_status(db, user_id: str, payload: UserUpdateStatus):
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"is_active": payload.is_active}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or status unchanged")
    doc = await db["users"].find_one({"_id": ObjectId(user_id)})
    return doc_to_user_res(doc)
