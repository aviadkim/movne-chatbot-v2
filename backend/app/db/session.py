from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# יצירת מחרוזת התחברות למסד הנתונים
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/"
    f"{settings.POSTGRES_DB}"
)

# יצירת מנוע מסד הנתונים
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,  # בדיקת חיבור לפני כל שימוש
        pool_size=5,  # גודל מאגר החיבורים
        max_overflow=10  # מספר חיבורים נוספים מעבר למאגר
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Failed to establish database connection: {str(e)}")
    raise

def get_db():
    """פונקציית עזר להשגת חיבור למסד הנתונים"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """אתחול מסד הנתונים"""
    from app.models.db_models import Base
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
