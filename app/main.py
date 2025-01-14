import uvicorn
from fastapi import FastAPI
from app.database import create_mongo_client

def init_app():
    app = FastAPI(
        title="Ryde Backend",
        description="best backend server in the world",
        version="0.0.1"
    )
    
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
    
    return app

app = init_app()

if __name__== "main":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)