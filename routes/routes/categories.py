from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Category, Word
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/categories")


@router.get("/")
async def all_categories(session: AsyncSession = Depends(get_async_session)):
    db_response = await session.execute(select(Category))

    categories = db_response.scalars().all()

    return {"data": categories}


@router.get("/{category_id}/words")
async def category_words(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Category)
        .where(Category.id == category_id)
        .options(selectinload(Category.words).selectinload(Word.translations))
    )

    data = await session.execute(query)
    return {
        "data": data.scalars().all()
    }
