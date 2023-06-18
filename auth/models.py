from sqlalchemy import *
from config.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    role = Column(String(50))

    def __str__(self):
        return f"{self.username}"
    
    