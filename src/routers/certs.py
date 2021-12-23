from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.ext.asyncio.session import AsyncSession

import schemas.certs as cert_schema
import cruds.certs as cert_crud
import cruds.hosts as host_crud
from db import get_db


router = APIRouter()


@router.get("/certs", response_model=List[cert_schema.Cert])
async def get_all_certs(db: AsyncSession = Depends(get_db)):
    return await cert_crud.get_all_certs(db)


@router.get("/cert/{cert_id}")
async def get_cert():
    pass


@router.post("/cert/{host_id}", response_model=cert_schema.CertCreateResponse)
async def create_cert(host_id: int, cert_body: cert_schema.CertCreate, db: AsyncSession = Depends(get_db)):
    host = await host_crud.get_host(db, host_id)
    return await cert_crud.create_cert(db, cert_body, host)


@router.delete("/cert/{cert_id}")
async def delete_cert():
    pass