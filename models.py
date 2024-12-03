from sqlalchemy import Column, Integer, String, CheckConstraint
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('edad >= 0', name='check_edad_positive'),
    )


