from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import certs
from db import Base


class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(1024), unique=True)

    certs = relationship("Cert", back_populates="hosts")