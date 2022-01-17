from sqlalchemy import Column, Integer, String

from db import Base


class Cert(Base):
    __tablename__ = "certs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(1024), unique=True)
    port = Column(Integer)
    begin_time = Column(String(256))
    expire_time = Column(String(256))
    begin_unixtime = Column(Integer)
    expire_unixtime = Column(Integer)
    issuer = Column(String(256))
    cert_state = Column(String(64))
    update_check_time = Column(String(256))

    def update(self, property_dict: dict):
        for key, value in property_dict.items():
            if key in self.__dict__:
                setattr(self, key, value)
