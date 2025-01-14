from fastapi import Depends
from app.users.models import User
from app.users.schema import UserCreate
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId
from app.main import get_database
import uuid

date_format = "%Y-%m-%d %H:%M:%S"

async def create_user(user: UserCreate,db: AsyncIOMotorDatabase = Depends(get_database)) -> User:
    user_collection = db.get_collection("users")
    user_dict = user.dict(by_alias=True)
    # user_dict["id"] = str(uuid.uuid4())  # Generate a random UUID for the user
    user_dict["createdAt"] = datetime.utcnow()
    # user_dict["dob"] = datetime.strptime(user_dict["dob"], date_format)

    user = await user_collection.insert_one(user_dict)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    print("new user", new_user)

    # converting _id to str from ObjectId
    new_user["_id"] = str(new_user["_id"])
    return User(**new_user)

async def get_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)) -> User:
    user_collection = db.get_collection("users")
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        # converting _id to str from ObjectId
        user["_id"] = str(user["_id"])
        return User(**user)

async def update_user(id: str, user_data: dict, db: AsyncIOMotorDatabase = Depends(get_database)) -> User:
    user_collection = db.get_collection("users")
    await user_collection.update_one({"_id": ObjectId(id)}, {"$set": user_data})
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        # converting _id to str from ObjectId
        user["_id"] = str(user["_id"])
        return User(**user)

async def delete_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    user_collection = db.get_collection("users")
    await user_collection.delete_one({"_id": ObjectId(id)})

async def get_friend_list(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    pass


async def get_nearby_friend_list(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    pass