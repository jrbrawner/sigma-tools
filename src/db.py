from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.settings import settings

if settings.ENVIRONMENT == "docker":
    POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}"
    engine = create_engine(POSTGRES_URL) # docker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
elif settings.ENVIRONMENT == "local":
    engine = create_engine(settings.DB_URI, connect_args={"check_same_thread": False}) #local, sqlite
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)
