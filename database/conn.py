from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from utils.get_parameter import get_ssm_parameter

database_host = get_ssm_parameter(name="/message-queue/dev/postgres/public_ip", default="localhost")

DATABASE_URL = f"postgresql://admin:password123@{database_host}:5432/mydb"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
