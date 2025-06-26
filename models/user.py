from sqlalchemy import Column, Integer, String, DateTime
from utils.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    create_at = Column(DateTime(timezone=True), nullable=False)
    image = Column(String(255), nullable=True)
