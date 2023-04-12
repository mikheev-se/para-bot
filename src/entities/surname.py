from sqlalchemy import Column, Integer, String
from src.entities.base import Base


class Surname(Base):
    __tablename__ = 'surnames'
    id = Column(Integer, primary_key=True)
    surname_ip = Column(String, index=True, unique=True)
    surname_rp = Column(String, index=True)
    surname_dp = Column(String, index=True)
    surname_vp = Column(String, index=True)
    surname_tp = Column(String, index=True)
    surname_pp = Column(String, index=True)
