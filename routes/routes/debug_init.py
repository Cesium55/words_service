from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import (
    Category,
    Language,
    Word,
    WordTranslation,
    Example,
    ExampleTranslation,
    category_word_table,
)
from managers.AuthManager import AuthManager
from managers.Logger import AsyncLogger
from pydantic import BaseModel
from typing import List
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload, joinedload
from brokers.broker import broker
from managers.WordsManager import WordsManager

from schemas.words import WordsReturnSchema
from schemas import words as words_schemas

router = APIRouter(prefix="/debug_init")
logger = AsyncLogger()
word_manager = WordsManager()


@router.get("/words", response_model=WordsReturnSchema)
async def get_words(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Word)
        .options(
            selectinload(Word.categories),
            selectinload(Word.translations).selectinload(WordTranslation.language),
            selectinload(Word.examples).selectinload(Example.translations),
        )
        .limit(20)
    )
    data = await session.execute(query)
    return {"data": data.scalars().all()}


@router.get("/")
def asdasd():
    return 123


@router.post("/init_public_key")
async def init_public_key():
    auth_manager = AuthManager()

    key = await auth_manager.public_key_init()
    return key


@router.get("/public_key")
async def get_public_key():
    await logger.info("get public key call")

    am = AuthManager()
    key = await am.get_auth_public_key()
    return key


#######################################################################

# Pydantic-схемы


class TranslationIn(BaseModel):
    lang: str
    text: str


class ExampleIn(BaseModel):
    lang: str
    text: str


class WordDataIn(BaseModel):
    transcription: str | None = None
    translations: List[TranslationIn]
    examples: List[ExampleIn] = []
    categories: List[str] = []


class WordImportPayload(BaseModel):
    data: List[WordDataIn]


################################################################
class WordDataInTemp(BaseModel):
    transcription: str | None = None
    translations: List[words_schemas.WordTranslationInput]
    examples: List[List[words_schemas.ExampleTranslationInput]] = []
    categories: List[str] = []


class WordImportPayloadTemp(BaseModel):
    data: List[WordDataInTemp]


@router.post("/import-words")
async def import_words(
    payload: WordImportPayload, session: AsyncSession = Depends(get_async_session)
):
    # Получаем языки в виде dict
    result = await session.execute(select(Language.id, Language.code))
    language_map = {code: id_ for id_, code in result.all()}

    # Получаем существующие категории
    result = await session.execute(
        select(Category.id, Category.name).where(Category.owner_id == None)
    )
    category_map = {name: id_ for id_, name in result.all()}

    # Словарь для сохранения новых категорий, чтобы не делать insert дубли
    new_categories = {}

    for word_data in payload.data:
        # 1. Создаём слово
        word = Word(transcription=word_data.transcription)
        session.add(word)
        await session.flush()  # Получаем ID

        # 2. Переводы
        for t in word_data.translations:
            lang_id = language_map.get(t.lang)
            if not lang_id:
                raise HTTPException(
                    status_code=400, detail=f"Unknown language code: {t.lang}"
                )
            session.add(
                WordTranslation(word_id=word.id, language_id=lang_id, text=t.text)
            )

        # 3. Примеры
        for ex in word_data.examples:
            lang_id = language_map.get(ex.lang)
            if not lang_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown language code in example: {ex.lang}",
                )
            example = Example(word_id=word.id)
            session.add(example)
            await session.flush()
            session.add(
                ExampleTranslation(
                    example_id=example.id, language_id=lang_id, text=ex.text
                )
            )

        # 4. Категории
        for cat_name in word_data.categories:
            cat_id = category_map.get(cat_name)
            if not cat_id:
                # Добавляем только 1 раз, если ещё не создана
                if cat_name in new_categories:
                    cat_id = new_categories[cat_name]
                else:
                    new_cat = Category(name=cat_name, owner_id=None)
                    session.add(new_cat)
                    await session.flush()
                    cat_id = new_cat.id
                    new_categories[cat_name] = cat_id
                    category_map[cat_name] = cat_id

            # Прямая вставка в связующую таблицу
            await session.execute(
                category_word_table.insert().values(category_id=cat_id, word_id=word.id)
            )

    await session.commit()
    return {"status": "success", "words_imported": len(payload.data)}


#######################################################################


@router.post("/create_my_cats")
async def create_my_cats(session: AsyncSession = Depends(get_async_session)):
    # cats = ["a2",
    # "preposition",
    # "pronoun",
    # "b1",
    # "conjunction",
    # "verb",
    # "modal verb",
    # "b2",
    # "determiner",
    # "indefinite article",
    # "definite article",
    # "adjective",
    # "a1",
    # "number",
    # "adverb",
    # "linking verb",
    # "noun",
    # "ordinal number",
    # "exclamation",
    # "c1",]

    cats = {
        "anatomy": "Анатомия",
        "animals": "Животные",
        "appearance": "Внешность",
        "archaeology": "Археология",
        "architecture": "Архитектура",
        "art": "Искусство",
        "basic_verbs": "Базовые глаголы",
        "business": "Бизнес",
        "career": "Карьера",
        "character": "Характер",
        "clothing": "Одежда",
        "colors": "Цвета",
        "computer": "Компьютер",
        "construction": "Строительство",
        "ecology": "Экология",
        "economy": "Экономика",
        "family": "Семья",
        "food": "Еда",
        "furniture": "Мебель",
        "geography": "География",
        "health": "Здоровье",
        "hobby": "Хобби",
        "home": "Дом, вещи",
        "idioms": "Идиомы",
        "irregular_verbs": "Неправильные глаголы",
        "legal_english": "Юриспруденция",
        "literature": "Литература",
        "marketing": "Маркетинг",
        "mass_media": "СМИ",
        "math": "Математика",
        "military_weapons": "Военное дело, оружие",
        "money": "Деньги",
        "movie": "Кино",
        "music": "Музыка",
        "numbers": "Числительные (колич.)",
        "numbers_ordinals": "Числительные (порядк.)",
        "oxford3000_a1": "Oxford 3000 - A1",
        "oxford3000_a2": "Oxford 3000 - A2",
        "oxford3000_b1": "Oxford 3000 - B1",
        "oxford3000_b2": "Oxford 3000 - B2",
        "oxford5000_b2": "Oxford 5000 - B2",
        "oxford5000_c1": "Oxford 5000 - C1",
        "photography": "Фотография",
        "phrasal_verbs": "Фразовые глаголы",
        "politics": "Политика",
        "psychology": "Психология",
        "signs_of_zodiac": "Знаки зодиака",
        "space": "Космос",
        "sport": "Спорт",
        "time": "Время",
        "time_days_of_week": "Дни недели",
        "time_months": "Месяцы",
        "time_seasons": "Времена года",
        "top100": "NGSL 1-100",
        "top1000": "NGSL 101-1000",
        "top3000": "NGSL 1001-3000",
        "town": "Город",
        "transport": "Транспорт",
        "travel": "Путешествия",
    }

    for i in cats:
        db_res = await session.execute(
            insert(Category).values({"name": i}).returning(Category)
        )
        new_cat = db_res.scalar_one_or_none()
        await broker.publish(
            {
                "name": i,
                "id": new_cat.id,
                "entity_name": "words",
            },
            "new_group_queue",
        )

    await session.commit()

    return 0


@router.post("/init_langs")
async def init_langs(session: AsyncSession = Depends(get_async_session)):
    stmt = (
        insert(Language)
        .values(
            [
                {"code": "rus", "name": "Русский"},
                {"code": "eng", "name": "English"},
                {"code": "spa", "name": "Español"},
                {"code": "deu", "name": "Deutsch"},
                {"code": "ita", "name": "Italiano"},
                {"code": "fra", "name": "Français"},
            ]
        )
        .returning(Language)
    )

    result = await session.execute(stmt)
    await session.commit()

    return result.scalars().all()


@router.post(
    "/add_words",
)
async def add_words(
    payload: WordImportPayloadTemp, session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Language.id, Language.code))
    language_map = {code: id_ for id_, code in result.all()}

    # Получаем существующие категории
    result = await session.execute(select(Category))
    category_map = {cat.name: cat.id for cat in result.scalars().all()}

    changed_data = []
    for word_data in payload.data:
        temp_categories = []
        for i in word_data.categories:
            temp_categories.append(category_map[i])

        changed_data.append(
            words_schemas.WordFullCreate(
                translations=word_data.translations,
                transcription=word_data.transcription,
                examples=word_data.examples,
                categories=temp_categories,
            )
        )

    result = await word_manager.full_create(
        session, words_schemas.WordsFullCreate(words=changed_data)
    )

    return result
