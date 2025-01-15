import os
import uvicorn
from fastapi import FastAPI, Depends
from app.database import create_mongo_client
from app.middleware.auth import AuthMiddleware, JWTBearer, sign_jwt
from dotenv import load_dotenv
load_dotenv()

def get_database():
    return app.mongodb_client

def init_app():
    app = FastAPI(
        title="Ryde Backend",
        description="best backend server in the world",
        version="0.0.1"
    )
    
    '''
    
    I have tested this auth middleware flow and it is working as expected
    but i am disabling this to impleted friends adding logic because with auth middlware
    i have to make changes in all  the router to consume requst object with user_id
    and that will transform all my controller funtions so for simplicity i am ignore that
    
    If i get the time i will complete full auth flow with pass word login
    
    '''
    # AUTH_SECRET = os.getenv("AUTH_SECRET")
    # app.add_middleware(AuthMiddleware, secret_key=AUTH_SECRET)
    
    @app.on_event("startup")
    async def startup_db_client():
        app.mongodb_client = create_mongo_client()

    @app.on_event("shutdown")
    async def shutdown_db_client():
        if app.mongodb_client is not None:
            app.mongodb_client.close()
    
    @app.get("/health-check")
    async def health_check():
        return "Welcome to Ryde Backend Server"
    
    #commneting this for now
    # @app.post("/get-token")
    # async def get_token(user_id: str):
    #     token = sign_jwt(user_id)
    #     return {"access_token": token, "token_type": "bearer"}

    from app.users.routes import router as users_router
    
    app.include_router(users_router)
    # app.include_router(users_router, dependencies=[Depends(JWTBearer())])

    return app

app = init_app()

if __name__== "main":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)