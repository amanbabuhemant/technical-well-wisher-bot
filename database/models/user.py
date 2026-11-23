from sqlalchemy import create_engine, Column, Integer, String, DateTime,func
from sqlalchemy.orm import DeclarativeBase, mapped_column
import json


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'


    id = mapped_column(Integer, primary_key=True)
    full_name = mapped_column(String(255), nullable=False)
    date_of_birth = mapped_column(String(5))
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())


    def __repr__(self):

        d = {
                "id": self.id,
                "full_name": self.full_name,
                "date_of_birth": self.date_of_birth,
                "created_at": str(self.created_at) ,
                "updated_at": str(self.updated_at)
            }

        return json.dumps(d, indent=2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth,
            "created_at": str(self.created_at) ,
            "updated_at": str(self.updated_at)
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_json_snippet(self):
        return f"```json\n{self.to_json()}\n```"

