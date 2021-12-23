from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio.session import async_session

import models.hosts as host_model
import schemas.hosts as host_schema
import cruds.certs as cert_crud


async def create_host(db: AsyncSession, host_create: host_schema.HostCreate) -> host_model.Host:
    print(host_create)
    host = host_model.Host(**host_create.dict())
    db.add(host)
    await db.commit()
    await db.refresh(host)
    return host


async def get_all_hosts(db: AsyncSession) -> List[Tuple[int, str]]:
    q = select(host_model.Host)
    result: Result = await db.execute(q)
    # Removal tuple 
    result_array = list(map(lambda x: x[0], result.all()))
    return result_array
    

async def get_host(db: AsyncSession, host_id: int) -> Tuple[int, str]:
    q = select(host_model.Host).filter(host_model.Host.id == host_id)
    result: Result = await db.execute(q)
    # Removal tuple
    filterd_host = result.first()[0]
    return filterd_host


async def update_host(db: AsyncSession, origin_host: host_model.Host, update_host: host_schema.HostCreate) -> host_model.Host:
    origin_host.domain = update_host.domain
    db.add(origin_host)
    await db.commit()
    await db.refresh(origin_host)
    return origin_host
    

async def delete_host(db: async_session, origin_host: host_model.Host) -> None:
    await db.delete(origin_host)
    await db.commit()