from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Category
from sqlalchemy import select

router = APIRouter(prefix="/categories")


@router.get("/")
async def all_categories(session: AsyncSession = Depends(get_async_session)):
    db_response = await session.execute(
        select(Category)
    )

    categories = db_response.scalars().all()

    return {"data": categories}
