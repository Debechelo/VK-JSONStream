from fastapi import FastAPI
from src.app.routers import router as api_router
from src.app.db.database import engine, Base
from src.app.db.model import Application

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)