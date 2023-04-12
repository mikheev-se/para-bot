from sqlalchemy import Column, Enum, Integer, String
from src.entities.base import Base


class Name(Base):
    __tablename__ = 'names'
    id = Column(Integer, primary_key=True)
    name_ip = Column(String, index=True, unique=True)
    name_rp = Column(String, index=True)
    name_dp = Column(String, index=True)
    name_vp = Column(String, index=True)
    name_tp = Column(String, index=True)
    name_pp = Column(String, index=True)
    sex = Column(Enum('М', 'Ж', name='ct_names_sex'))
