from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime

CategoryType = Literal[
    "salary", "freelance", "investment", "food", 
    "travel", "rent", "shopping", "medical", 
    "entertainment", "utilities"
]

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: str = Field(..., pattern="^(income|expense)$")
    category: CategoryType
    date: datetime
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(income|expense)$")
    category: Optional[CategoryType] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class RecordResponse(RecordBase):
    id: str
    created_by: str
    created_at: datetime
    
    model_config = ConfigDict(populate_by_name=True)
