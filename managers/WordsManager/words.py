from sqlalchemy.ext.asyncio import AsyncSession
from models import Word, Category, Example, WordTranslation
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List


class WordsManager:

    def __init__(self): ...

    async def get_all(self, session: AsyncSession):
        db_response = await session.execute(select(Word))
        return db_response.scalars().all()

    async def get_by_ids(self, ids: List[int], session: AsyncSession):
        """Get words by list of ids"""

        query = (
            select(Word)
            .where(Word.id.in_(set(ids)))
            .options(
                selectinload(Word.categories),
                selectinload(Word.translations).selectinload(WordTranslation.language),
                selectinload(Word.examples).selectinload(Example.translations),
            )
        )

        db_response = await session.execute(query)
        return db_response.scalars().all()
