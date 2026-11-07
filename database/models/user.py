from sqlalchemy import create_engine, Column, Integer, String, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()


class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    date_of_birth = Column(String(5))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f"<User(full_name='{self.full_name}', date_of_birth='{self.date_of_birth}'"


