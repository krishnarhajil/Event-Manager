from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine, autoflush = False)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)