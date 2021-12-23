from typing import List, Tuple
import ssl
import socket
import datetime
from urllib.parse import urlparse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio.session import async_session

import models.certs as cert_model
import schemas.certs as cert_schema


async def create_cert(db: AsyncSession, cert_body: cert_schema.CertCreate) -> cert_model.Cert:
    cert_controller = CertController(cert_body)
    cert_data = await cert_controller.getCertData()
    cert = cert_model.Cert(**cert_data)

    db.add(cert)
    await db.commit()
    await db.refresh(cert)
    return cert


async def get_all_certs(db: AsyncSession) -> List[Tuple[int, str]]:
    q = select(cert_model.Cert)
    result: Result = await db.execute(q)
    # Removal tuple 
    result_array = list(map(lambda x: x[0], result.all()))
    return result_array


async def get_cert(db: AsyncSession, cert_id: int) -> Tuple[int, str]:
    q = select(cert_model.Cert).filter(cert_model.Cert.id == cert_id)
    result: Result = await db.execute(q)
    # Removal tuple
    filterd_cert = result.first()[0]
    return filterd_cert


async def expiry_check_cert(db: AsyncSession, origin_cert: cert_model.Cert) -> cert_model.Cert:
    schema = cert_schema.CertCreate(domain=origin_cert.domain, port=origin_cert.port)
    cert_controller = CertController(schema)
    renew_cert_data = await cert_controller.getCertData()
    origin_cert.update(renew_cert_data) 
    db.add(origin_cert)
    await db.commit()
    await db.refresh(origin_cert)
    return origin_cert


async def delete_cert(db: async_session, origin_cert: cert_model.Cert) -> None:
    await db.delete(origin_cert)
    await db.commit()



class CertController():

    def __init__(self, cert: cert_schema.CertCreate) -> None:
        self.domain = cert.domain
        self.port = cert.port
        self.fmt= r"%b %d %H:%M:%S %Y %Z"
        self.ssl_info = None
    

    async def __getSSLCertInfo(self) -> dict:
        port = self.port
        host = self.domain
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = host) as conn:
            conn.settimeout(5)
            conn.connect((host, port))
            return conn.getpeercert()
    
    
    def getSSLCertBeginTime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.ssl_info["notBefore"], self.fmt)


    def getSSLCertExpireTime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.ssl_info["notAfter"], self.fmt)


    def getSSLCertBeginUnixTime(self) -> datetime.datetime:
        return int(datetime.datetime.strptime(self.ssl_info["notBefore"], self.fmt).timestamp())


    def getSSLCertExpireUnixTime(self) -> datetime.datetime:
        return int(datetime.datetime.strptime(self.ssl_info["notAfter"], self.fmt).timestamp())


    def getSSLCertIssuer(self) -> str:
        return self.ssl_info["issuer"][1][0][1]

 
    def getSSLCertState(self) -> str:
        nowtime = datetime.datetime.now()
        expire_date = self.getSSLCertExpireTime()
        delta = expire_date - nowtime
        days_left = delta.days
        # Fine
        if days_left >= 30:
            return "Fine"
        # Expired
        elif days_left < 0:
            return "Expired"
        # Danger
        elif days_left < 10:
            return "Danger"
        # Warning
        elif days_left < 30:
            return "Warning"


    async def getCertData(self) -> dict:
        self.ssl_info = await self.__getSSLCertInfo()
        cert = {
            "domain" : self.domain,
            "port" : self.port,
            "begin_time" : self.getSSLCertBeginTime(),
            "expire_time" : self.getSSLCertExpireTime(),
            "begin_unixtime" : self.getSSLCertBeginUnixTime(),
            "expire_unixtime" : self.getSSLCertExpireUnixTime(),
            "cert_state" : self.getSSLCertState(),
            "issuer" : self.getSSLCertIssuer(),
            "update_check_time" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return cert
