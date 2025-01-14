from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#will use this schema to accept create-user api body
class UserCreate(BaseModel):
    name: str
    dob: Optional[str]
    address: Optional[str]
    description: Optional[str]

# use this to validate update api body
class UserUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

# this is schema for return response of user data
class UserResponse(BaseModel):
    id: str
    name: str
    dob: Optional[str]
    address: Optional[str]
    description: Optional[str]
    createdAt: datetime