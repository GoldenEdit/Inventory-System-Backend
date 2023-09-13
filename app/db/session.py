from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

<<<<<<< Updated upstream
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
=======

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
>>>>>>> Stashed changes
