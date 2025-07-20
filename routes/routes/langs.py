from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Language
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from middleware.AuthMiddleware import user_required


router = APIRouter(prefix="/languages")


@router.get("/")
async def all_langs(session: AsyncSession = Depends(get_async_session)):

    return (await session.execute(select(Language))).scalars().all()
