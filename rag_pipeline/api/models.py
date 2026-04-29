from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(120))
    address = Column(String(200))
    pin_code = Column(String(10))
    is_admin = Column(Boolean, default=False)