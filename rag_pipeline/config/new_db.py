from sqlalchemy import create_all, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./rag.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use this to initialize the tables
def init_db():
    from api.models import Base
    Base.metadata.create_all(bind=engine)