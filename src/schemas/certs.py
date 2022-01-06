from typing import Optional, List
from pydantic import BaseModel, Field


class Cert(BaseModel):
    id: int
    domain: str = Field(None, example="www.example.com", description="Domain Name")
    port: int = Field(None, example=443, description="Port Number")
    begin_time: str = Field(None, example="1970-01-01 00:00:00", description="Begin SSLCert time")
    expire_time: str = Field(None, example="2038-01-19 03:14:07", description="Expire SSLCert time")
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
    update_check_time: str = Field(None, example="2038-01-19 00:00:00", description="Cert Last Check Time")

    class Config:
        orm_mode = True


class CertCreate(BaseModel):
    domain: str = Field(None, example="www.example.com", description="Domain Name")
    port: int = Field(None, example=443, description="Port Number")

    class Config:
        orm_mode = True


class CertCreateResponse(Cert):
    pass


class CertUpdateResponse(BaseModel):
    id: int
    domain: str = Field(None, example="www.example.com", description="Domain Name")
    port: int = Field(None, example=443, description="Port Number")
    begin_time: str = Field(None, example="1970-01-01 00:00:00" , description="Begin SSLCert time")
    expire_time: str = Field(None, example="2038-01-19 03:14:07" , description="Expire SSLCert time")
    update_check_time: str = Field(None, example="2038-01-19 00:00:00", description="Cert Last Check Time")

    class Config:
        orm_mode = True


class CertExpiryCheckResponse(BaseModel):
    id: int
    result: bool = Field(None, example="True", description="Cert Check Result")
    domain: str = Field(None, example="www.example.com", description="Domain Name")
    port: int = Field(None, example=443, description="Port Number")
    message: Optional[str] = Field(None, example="[Errno 2] No such file or directory: 'not_exist_file'", description="Reason for Exception")


class AllCertExpiryCheckResponse(BaseModel):
    cert_size: int = Field(None, example="777", description="Checked number of cert")
    error: Optional[List[CertExpiryCheckResponse]]
