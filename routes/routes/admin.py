from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Category, Language
from middleware.AuthMiddleware import admin_required
from schemas.languages import LanguageCreate
from schemas.words import WordsImportRequest
from typing import List

from services.LanguageService import LanguageService
from services import AdminCRUDService


router = APIRouter(prefix="/admin", dependencies=[Depends(admin_required)])


@router.get("/")
async def admin_index():
    return {"message": "Welcome admin!"}


@router.post(
    "/languages",
    # response_model=LanguageCreate,
    status_code=201,
    # dependencies=[Depends(admin_required)],
)
async def create_language(
    language_data: LanguageCreate, session: AsyncSession = Depends(get_async_session)
):
    return await LanguageService().create_language(language_data, session)
