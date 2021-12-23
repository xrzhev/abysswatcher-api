from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import hosts
from db import Base


class Cert(Base):
    __tablename__ = "certs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey("hosts.id"))
    port = Column(Integer)
    begin_time = Column(String(256))
    expire_time = Column(String(256))
    begin_unixtime = Column(Integer)
    expire_unixtime = Column(Integer)
    issuer = Column(String(256))
    cert_state = Column(String(64))
    update_check_time = Column(String(256))

    hosts = relationship("Host", back_populates="certs")
