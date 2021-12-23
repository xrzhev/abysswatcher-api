from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.ext.asyncio.session import AsyncSession

import schemas.certs as cert_schema
import cruds.certs as cert_crud
from db import get_db


router = APIRouter()


@router.get("/certs", response_model=List[cert_schema.Cert])
async def get_all_certs(db: AsyncSession = Depends(get_db)):
    return await cert_crud.get_all_certs(db)


@router.get("/cert/{cert_id}")
async def get_cert(cert_id: int, db: AsyncSession = Depends(get_db)):
    return await cert_crud.get_cert(db, cert_id)


@router.post("/cert/", response_model=cert_schema.CertCreateResponse)
async def create_cert(cert_body: cert_schema.CertCreate, db: AsyncSession = Depends(get_db)):
    return await cert_crud.create_cert(db, cert_body)


@router.put("/cert/{cert_id}", response_model=cert_schema.CertCreateResponse)
async def update_cert(cert_id: int, cert_body: cert_schema.CertCreate, db: AsyncSession = Depends(get_db)):
    return await cert_crud.create_cert(db, cert_body)


@router.put("/cert/check/{cert_id}", response_model=cert_schema.CertUpdateResponse)
async def expiry_check_cert(cert_id: int, db: AsyncSession = Depends(get_db)):
    origin_cert = await cert_crud.get_cert(db, cert_id)
    return await cert_crud.expiry_check_cert(db, origin_cert)
    


@router.put("/cert/check/all", response_model=cert_schema.CertUpdateResponse)
async def bulk_expiry_check_cert(db: AsyncSession = Depends(get_db)):
    pass


@router.delete("/cert/{cert_id}")
async def delete_cert(cert_id: int, db: AsyncSession = Depends(get_db)):
    origin_cert = await cert_crud.get_cert(db, cert_id)
    return await cert_crud.delete_cert(db, origin_cert)
