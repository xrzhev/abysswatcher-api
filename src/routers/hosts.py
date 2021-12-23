from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from sqlalchemy.ext.asyncio.session import AsyncSession

import schemas.hosts as host_schema
import schemas.certs as cert_schema 
import cruds.hosts as host_crud
import cruds.certs as cert_crud
from db import get_db


router = APIRouter()


@router.get("/hosts", response_model=List[host_schema.Host])
async def get_all_hosts(db: AsyncSession = Depends(get_db)):
    return await host_crud.get_all_hosts(db)


@router.get("/host/{host_id}", response_model=host_schema.Host)
async def get_host(host_id: int, db: AsyncSession = Depends(get_db)):
    return await host_crud.get_host(db, host_id)


@router.post("/host", response_model=host_schema.HostCreateResponse)
async def create_host(host: host_schema.HostCreate, cert: cert_schema.CertCreate,  db: AsyncSession = Depends(get_db)):
    resp_host = await host_crud.create_host(db, host)
    await cert_crud.create_cert(db, cert, resp_host)
    return resp_host


@router.put("/host/{host_id}", response_model=host_schema.HostCreateResponse)
async def update_host(host_id: int, host_body: host_schema.HostCreate, db: AsyncSession = Depends(get_db)):
    origin_host = await host_crud.get_host(db, host_id)
    return await host_crud.update_host(db, origin_host, host_body)


@router.delete("/host/{host_id}", response_model=None)
async def delete_host(host_id: int, db:AsyncSession = Depends(get_db)):
    origin_host = await host_crud.get_host(db, host_id)
    return await host_crud.delete_host(db, origin_host)

