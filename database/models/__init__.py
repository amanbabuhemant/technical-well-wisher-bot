from .user import User
from sqlalchemy import engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///../bot.db',echo= True)
from .user import Base 


Base.metadata.create_all(engine)

