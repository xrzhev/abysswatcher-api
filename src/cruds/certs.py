from typing import List
import datetime
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

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


async def get_all_certs(db: AsyncSession) -> List[cert_model.Cert]:
    q = select(cert_model.Cert)
    result: Result = await db.execute(q)
    # Removal tuple 
    result_array = list(map(lambda x: x[0], result.all()))
    return result_array


async def get_cert(db: AsyncSession, cert_id: int) -> cert_model.Cert:
    q = select(cert_model.Cert).filter(cert_model.Cert.id == cert_id)
    result: Result = await db.execute(q)
    # Removal tuple
    filterd_cert = result.first()[0]
    return filterd_cert


async def update_cert(db: AsyncSession, origin_cert: cert_model.Cert, update_schema: cert_schema.CertCreate) -> cert_model.Cert:
    cert_controller = CertController(update_schema)
    renew_cert_data = await cert_controller.getCertData()
    origin_cert.update(renew_cert_data)
    db.add(origin_cert)
    await db.commit()
    await db.refresh(origin_cert)
    return origin_cert


async def delete_cert(db: AsyncSession, origin_cert: cert_model.Cert) -> None:
    await db.delete(origin_cert)
    await db.commit()


async def expiry_check_cert(db: AsyncSession, origin_cert: cert_model.Cert) -> cert_model.Cert:
    schema = cert_schema.CertCreate(domain=origin_cert.domain, port=origin_cert.port)
    cert_controller = CertController(schema)
    renew_cert_data = await cert_controller.getCertData()
    origin_cert.update(renew_cert_data) 
    db.add(origin_cert)
    await db.commit()
    await db.refresh(origin_cert)
    return origin_cert


async def expiry_check_all_certs(db: AsyncSession) -> List[cert_model.Cert]:

    async def task_runner(db: AsyncSession, origin_cert: cert_model.Cert, cert_schema: cert_schema.CertCreate):
        cert_controller = CertController(cert_schema)
        renew_cert_data = await cert_controller.getCertData()
        origin_cert.update(renew_cert_data)
        db.add(origin_cert)
        return renew_cert_data

    task_list = []
    certs = await get_all_certs(db)
    for cert in certs:
        schema = cert_schema.CertCreate(domain=cert.domain, port=cert.port)
        task_list.append(task_runner(db, cert, schema))
    return_array = await asyncio.gather(*task_list)
    print(return_array)
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
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.create_connection(asyncio.Protocol, host, port, ssl=True)
        return transport.get_extra_info("peercert")
 

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
