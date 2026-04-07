from sqlalchemy import Column, Integer, String
from db import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    movie_name = Column(String)
    hero = Column(String)
    heroine = Column(String)

Base.metadata.create_all(bind=engine)