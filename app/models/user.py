from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

""" 
Модель пользователя
"""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


tasks = relationship("Task", back_populates="owner")
