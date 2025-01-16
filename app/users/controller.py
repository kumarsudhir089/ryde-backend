from fastapi import Depends
from app.users.models import User, FriendsRelation
from app.users.schema import UserCreate, FriendRequestObj
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId
from app.main import get_database
from app.utility.distanceCalulator import haversine
import uuid


date_format = "%Y-%m-%d %H:%M:%S"

async def create_user(user: UserCreate,db: AsyncIOMotorDatabase = Depends(get_database)) -> User:
    user_collection = db.get_collection("users")
    user_dict = user.dict(by_alias=True)
    # user_dict["id"] = str(uuid.uuid4())  # Generate a random UUID for the user
    user_dict["createdAt"] = datetime.utcnow()

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


async def make_friends(connectionObj: FriendRequestObj, db: AsyncIOMotorDatabase = Depends(get_database)):
    follow_collection = db.get_collection("follows")
    friend_dict = connectionObj.dict(by_alias=True)
    friend_dict["createdAt"] = datetime.utcnow()

    '''
    lets check if this connection already exists in DB
    '''
    
    existing_connection = await follow_collection.find_one({
        "user_id": connectionObj.user_id,
        "friend_id": connectionObj.friend_id
    })

    if existing_connection:
        raise ValueError("This connection already exists")


    '''
    connection doesnt exist in db, so we can proceed
    '''
    follow_edge = await follow_collection.insert_one(friend_dict)
    newEdge = await follow_collection.find_one({"_id": follow_edge.inserted_id})
    # print("new user", newEdge)

    # converting _id to str from ObjectId
    newEdge["_id"] = str(newEdge["_id"])
    return FriendsRelation(**newEdge)

async def remove_friends(connectionObj: FriendRequestObj, db: AsyncIOMotorDatabase = Depends(get_database)):
    follow_collection = db.get_collection("follows")
    
    '''
    lets check if this connection already exists in DB
    '''
    existing_connection = await follow_collection.find_one({
        "user_id": connectionObj.user_id,
        "friend_id": connectionObj.friend_id
    })
    
    if existing_connection:
        await follow_collection.delete_one({
            "user_id": connectionObj.user_id,
            "friend_id": connectionObj.friend_id
        })
    else:
        raise ValueError("This connection doesn't  exists")

async def get_friend_list(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    follow_collection = db.get_collection("follows")
    
    
    ## started with step by step approach, but read the we can do it single query using aggs
    # following = await follow_collection.find({"user_id": id}).to_list(length=None)
    # following_ids = {follow["friend_id"] for follow in following}
    
    # # Find all users that follow the given user
    # followers = await follow_collection.find({"friend_id": id}).to_list(length=None)
    # follower_ids = {follow["user_id"] for follow in followers}
    
    # # Find mutual followers (friends)
    # friends_ids = following_ids.intersection(follower_ids)
    
    # # Fetch friend details
    # user_collection = db.get_collection("users")
    # friends = await user_collection.find({"_id": {"$in": list(friends_ids)}}).to_list(length=None)
    

    pipeline = [
        {
            "$match": {"user_id": id}  # Match relations for the given user
        },
        {
            "$lookup": {
                "from": "follows",
                "let": {"friend_id": "$friend_id", "user_id": "$user_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$user_id", "$$friend_id"]},  # Reverse relationship
                                    {"$eq": ["$friend_id", id]}
                                ]
                            }
                        }
                    }
                ],
                "as": "reverse_relation"  # Check if reverse relation exists
            }
        },
        {
            "$match": {"reverse_relation": {"$ne": []}}  # Only keep friends with reverse relation
        },
        {
            "$addFields": {
                "friend_id_obj": {"$toObjectId": "$friend_id"}  # Convert friend_id to ObjectId
            }
        },
        {
            "$lookup": {
                "from": "users",  # Lookup user details
                "localField": "friend_id_obj",
                "foreignField": "_id",
                "as": "friend_details"
            }
        },
        {
            "$unwind": "$friend_details"  # Flatten the friend_details array
        },
        {
            "$replaceRoot": {
                "newRoot": "$friend_details"
            }
        }
    ]
    
    friends = await follow_collection.aggregate(pipeline).to_list(length=None)
    for friend in friends:
        friend["_id"] = str(friend["_id"])
    return friends


async def get_nearby_friend_list(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    friendsList = await get_friend_list(id, db)
    user = await get_user(id, db)
    
    if not user:
        return []
    
    user_lat = user.get("latitude")
    user_lon = user.get("longitude")

    if user_lat is None or user_lon is None:
        return []

    for friend in friendsList:
        friend_lat = friend.get("latitude")
        friend_lon = friend.get("longitude")
        if friend_lat is not None and friend_lon is not None:
            friend["distance"] = haversine(user_lat, user_lon, friend_lat, friend_lon)
        else:
            friend["distance"] = float('inf')

    friendsList.sort(key=lambda x: x["distance"])
    return friendsList