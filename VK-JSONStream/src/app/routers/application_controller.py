from fastapi import APIRouter, HTTPException, Depends
from src.app.models.application import Application as application
from sqlalchemy.orm import Session
from src.app.db.database import get_db

router = APIRouter()


@router.post("/application/", response_model=application)
async def create_application(item: application, db: Session = Depends(get_db)):
    db_item = application(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/application/{item_id}/configuration", response_model=application)
async def update_application_configuration(item_id: int, config: dict, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.configuration = config
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("application/{item_id}/settings", response_model=application)
async def update_application_settings(item_id: int, settings: dict, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.settings = settings
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("application/{item_id}/state", response_model=application)
async def update_application_state(item_id: int, state: str, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.state = state
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("application/{item_id}", response_model=application)
async def delete_application(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item


@router.get("application/{item_id}", response_model=application)
async def get_application(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("application/{item_id}/state", response_model=str)
async def get_application_state(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(application).filter(application.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item.state
