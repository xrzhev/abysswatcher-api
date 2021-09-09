import datetime
from pydantic import BaseModel, HttpUrl
from typing import List
import datetime

class generateCertClass(BaseModel):
    url: HttpUrl
    port: int


class RegisterCert(BaseModel):
    url:  HttpUrl
    port: int
    sslCertBeginDate: datetime.datetime
    sslCertExpireDate: datetime.datetime
    sslCertBeginUnixTime: int
    sslCertExpireUnixTime: int
    sslCertIssuer: str
    sslCertState: int
    updateCheckTime: datetime.datetime = datetime.datetime.now()