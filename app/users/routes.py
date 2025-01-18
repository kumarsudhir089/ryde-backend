from fastapi import APIRouter, HTTPException, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.users.schema import UserCreate, UserUpdate, UserResponse, FriendRequestObj
from app.users.controller import create_user, get_user, update_user, delete_user,make_friends, remove_friends, get_friend_list, get_nearby_friend_list
from app.main import get_database

router = APIRouter(
    prefix="/v1/user",
    tags=["users"]
)

@router.post("/", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await create_user(user, db)
    return user

@router.get("/{id}", response_model=UserResponse)
async def get_user_route(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    '''
    commented code belongs to user auth middleware flow
    currently i commneted this after testing because
    to enable this i need to make full project changes 
    in all routers to consume request object
    as i am hiding user_ids in auth header bearer token
    '''
    # # print("user id", request.state.user)
    # id = dict(request.state.user)["user_id"]
    user = await get_user(id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", response_model=UserResponse)
async def update_user_route(id: str, user: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_database)):
    updated_user = await update_user(id, user.dict(exclude_unset=True), db)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/friend")
async def remove_friends_route(connectionObj: FriendRequestObj, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        await remove_friends(connectionObj, db)
        return {"message": "Connection Removed!!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.delete("/{id}")
async def delete_user_route(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    await delete_user(id, db)
    return {"message": "User deleted successfully"}


@router.post("/make-friend")
async def make_friends_route(connectionObj: FriendRequestObj, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        await make_friends(connectionObj, db)
        return {"message": "Connected!!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/friend/{id}")
async def get_friends_for_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        friendsList = await get_friend_list(id, db)
        return friendsList
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/nearby-friend/{id}")
async def get_nearby_friends_for_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    pass

