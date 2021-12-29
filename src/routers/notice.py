from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
import cruds.notice 
from db import get_db

router = APIRouter()


@router.post("/notice/slack")
async def slack_notice(db: AsyncSession = Depends(get_db)):
    return await cruds.notice.do_notice(db)

