from fastapi import APIRouter

router = APIRouter()


@router.post("/notice/slack")
async def slack_notice():
    pass