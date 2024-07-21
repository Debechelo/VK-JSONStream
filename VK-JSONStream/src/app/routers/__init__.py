from fastapi import APIRouter
from .application_controller import router as application_router

router = APIRouter()

router.include_router(application_router, prefix="/applications", tags=["applications"])
