from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

get_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()