from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///sqlite.db"

engine= create_engine(DATABASE_URL)

Sessionlocal = sessionmaker(bind=engine,expire_on_commit= False)


session = Sessionlocal()

class Base(DeclarativeBase):
    ...