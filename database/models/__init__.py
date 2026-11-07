from .user import User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../bot.db')
# Create all tables in the engine 


Base = declarative_base()


Base.metadata.create_all(engine)


