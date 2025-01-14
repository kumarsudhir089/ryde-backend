from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#will extend this later to get friends and geo location data
class User(BaseModel):
    id: str = Field(..., alias="_id", primary_key=True)
    name: str
    dob: Optional[str]
    address: Optional[str]
    description: Optional[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    latitude: int = None
    longitude: int = None

class FriendsRelation(BaseModel):
    id: str = Field(..., alias="_id", primary_key=True)
    user_id: str = Field(...)
    friend_id: str = Field(...)
    createdAt: datetime = Field(default_factory=datetime.utcnow)