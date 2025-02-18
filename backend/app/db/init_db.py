from sqlalchemy.orm import Session
from ..db.session import engine
from ..models.base import Base

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
