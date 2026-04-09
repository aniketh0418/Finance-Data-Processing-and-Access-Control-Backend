from datetime import datetime, timezone
from typing import Optional

def doc_to_user_res(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "role": doc.get("role"),
        "is_active": doc.get("is_active"),
        "created_at": doc.get("created_at")
    }

def create_user_doc(name: str, email: str, password_hash: str, role: str = "viewer") -> dict:
    return {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "role": role,
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }
