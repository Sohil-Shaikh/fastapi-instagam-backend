from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://postgres:root@localhost"

engine= create_engine(DATABASE_URL,echo=True)

Sessionlocal = sessionmaker(bind=engine, expire_on_commit= False)


session = Sessionlocal()

class Base(DeclarativeBase):
    ...