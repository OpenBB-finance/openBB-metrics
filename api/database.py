from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utilities.config import settings

user = settings.POSTGRES_USERNAME
password = settings.POSTGRES_PASSWORD
# host = settings.POSTGRES_URL
host = "db"
db_name = settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db_name}'

# TODO: is the pool_size enough?
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=25, echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
