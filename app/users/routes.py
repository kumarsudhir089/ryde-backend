from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.users.schema import UserCreate, UserUpdate, UserResponse
from app.users.controller import create_user, get_user, update_user, delete_user
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

@router.delete("/{id}")
async def delete_user_route(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    await delete_user(id, db)
    return {"message": "User deleted successfully"}