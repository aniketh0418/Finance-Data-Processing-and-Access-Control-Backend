from datetime import datetime, timezone
from typing import Optional

def doc_to_record_res(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "amount": doc.get("amount"),
        "type": doc.get("type"),
        "category": doc.get("category"),
        "date": doc.get("date"),
        "notes": doc.get("notes"),
        "created_by": str(doc.get("created_by")),
        "created_at": doc.get("created_at")
    }

def create_record_doc(record_data: dict, user_id: str) -> dict:
    doc = record_data.copy()
    doc["created_by"] = user_id
    doc["created_at"] = datetime.now(timezone.utc)
    # Ensure date is a datetime object
    if isinstance(doc.get("date"), str):
        doc["date"] = datetime.fromisoformat(doc["date"].replace("Z", "+00:00"))
    return doc
