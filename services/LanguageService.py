from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Language
from schemas.languages import LanguageCreate
from database import get_async_session


class LanguageService:
    async def create_language(
        self,
        language_data: LanguageCreate,
        session: AsyncSession = Depends(get_async_session),
    ):
        result = await session.execute(
            select(Language).where(Language.code == language_data.code)
        )
        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=409, detail="Language code already exists")

        new_language = Language(code=language_data.code, name=language_data.name)
        session.add(new_language)
        await session.commit()
        await session.refresh(new_language)

        return new_language
