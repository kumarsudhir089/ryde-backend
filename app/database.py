import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()

# TODO: lets move this to env later
MONGO_URL = os.getenv("MONGO_URL")

def create_mongo_client():
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        database = client.ryde
        print("--------Connected to Mongo----------")
        return database
    except:
        print('Some Trouble connecting with Mongo')
        return None