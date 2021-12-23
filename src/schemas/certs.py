from pydantic import BaseModel, Field
from sqlalchemy.sql.expression import desc

class Cert(BaseModel):
    id: int
    host_id: int
    port: int = Field(None, example=443, description="PortNumber")
    begin_time: str = Field(None, example="1970-01-01 00:00:00" , description="Begin SSLCert time")
    expire_time: str = Field(None, example="2038-01-19 03:14:07" , description="Expire SSLCert time")
    begin_unixtime: int  =  Field(None, example=0, description="Begin SSLCert unixtime")
    expire_unixtime: int = Field(None, example=2147483647, description="Expire SSLCert unixtime")
    issuer: str = Field(None, example="Let's Encript", description="SSLCert Issuer")
    cert_state: str = Field(None, example="Fine", description="""
        SSL Certificate state
        * Expire_left_days >= 30: Fine
        * Expire_left_days > 15 : Warning
        * Expire_left_days > 7  : Danger
        * Expire_left_days <= 0 : Expired
    """)

    class Config:
        orm_mode = True

class CertCreate(BaseModel):
    port: int

    class Config:
        orm_mode = True


class CertCreateResponse(Cert):
    pass

    class Config:
        orm_mode = True

