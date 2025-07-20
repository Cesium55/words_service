from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models import Category
from typing import List


class CategoriesManager:

    async def get_system_categories(self, session: AsyncSession):
        query = select(Category).where(Category.owner_id == -1)
        db_result = await session.execute(query)
        categories = db_result.scalars().all()
        return categories

    async def get_allowed_categories(self, session: AsyncSession, owner_id):
        query = select(Category).where(Category.owner_id.in_(set([-1, owner_id])))
        db_result = await session.execute(query)
        categories = db_result.scalars().all()
        return categories

    async def check_permissions(
        self, session: AsyncSession, owner_id: int, cats_ids: List[int]
    ):
        query = select(Category).where(Category.id.in_(cats_ids))
        db_result = await session.execute(query)
        cats = db_result.scalars().all()

        for i in cats:
            if (owner_id == -1) or (owner_id == i.id):
                continue
            else:
                return False
        return True
