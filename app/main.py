import uvicorn
from fastapi import FastAPI

def init_app():
    app = FastAPI(
        title="Ryde Backend",
        description="best backend server in the world",
        version="0.0.1"
    )
    
    @app.get("/health-check")
    async def health_check():
        return "Welcome to Ryde Backend Server"
    
    return app

app = init_app()

if __name__== "main":
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)