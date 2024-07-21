from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
from sqlalchemy.sql import func
from src.app.db.database import Base


class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    version = Column(String(255), nullable=False)
    configuration = Column(JSON, nullable=False)
    settings = Column(JSON)
    state = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())