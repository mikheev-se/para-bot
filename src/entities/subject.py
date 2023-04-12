from sqlalchemy import Column, Integer, String
from src.entities.base import Base


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject = Column(String, index=True)
    lemma = Column(String, index=True)
    acronym = Column(String, index=True)
