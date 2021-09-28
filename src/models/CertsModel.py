import datetime
from pydantic import BaseModel, HttpUrl
from typing import List
import datetime

class GenerateCertModel(BaseModel):
    url: HttpUrl
    port: int


class RegisterCertModel(BaseModel):
    url:  HttpUrl
    port: int
    sslCertBeginDate: datetime.datetime
    sslCertExpireDate: datetime.datetime
    sslCertBeginUnixTime: int
    sslCertExpireUnixTime: int
    sslCertIssuer: str
    sslCertState: int
    updateCheckTime: datetime.datetime


class UpdateCertModel(BaseModel):
    cert_id: int