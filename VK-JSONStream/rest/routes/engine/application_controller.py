from fastapi import APIRouter
from rest.models.engine.application import Application as application
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/application/", response_model=application)
async def create_application(item: application):
    pass
    
    
@router.put("/application/{item_id}/configuration", response_model=application)
async def update_application_configuration(item_id: str, config: dict):
    pass
    

@router.put("/application/{item_id}/settings", response_model=application)
async def update_application_settings(item_id: str, settings: dict):
    pass
    

@router.put("/application/{item_id}/state", response_model=application)
async def update_application_state(item_id: str, state: str):
    pass
    

@router.delete("/application/{item_id}", response_model=application)
async def delete_application(item_id: str):
    pass
    

@router.get("/application/{item_id}", response_model=application)
async def get_application(item_id: str):
    pass
    

@router.get("/application/{item_id}/state", response_model=str)
async def get_application_state(item_id: str):
    pass
