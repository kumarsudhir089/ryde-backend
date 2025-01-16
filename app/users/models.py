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
    # these are added later for additional requirements
    latitude: int = None
    longitude: int = None


'''
I am assuming here is that friendship is directional, meaning:
if a is connected with b and b is conneted with a 
    then they are friends
else:
    if a is connected to b and b is not connected to a and vice versa:
        then  they re not friends a or b just follows the other person

so when i will fetch friends for "a" then i will check for both direction 
'''
class FriendsRelation(BaseModel):
    id: str = Field(..., alias="_id", primary_key=True)
    user_id: str = Field(...)
    friend_id: str = Field(...)
    createdAt: datetime = Field(default_factory=datetime.utcnow)