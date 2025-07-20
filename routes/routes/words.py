from fastapi import APIRouter, Depends
from managers.WordsManager import WordsManager
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.words import WordsByIDs, WordsReturnSchema

router = APIRouter(prefix="/words")

wm = WordsManager()


@router.get("/")
async def get_all_words(session: AsyncSession = Depends(get_async_session)):

    return {"data": await wm.get_all(session)}


@router.get("/ids")
async def get_ids(session: AsyncSession = Depends(get_async_session)):

    return {"data": await wm.get_ids(session)}


@router.post("/by-ids", response_model=WordsReturnSchema)
async def words_by_ids(
    ids: WordsByIDs, session: AsyncSession = Depends(get_async_session)
):
    return {"data": await wm.get_by_ids(ids.ids, session)}
