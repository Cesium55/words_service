from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from models import Category

router = APIRouter(prefix="/debug_init")


# @router.post("/create_my_cats")
# async def create_my_cats(session: AsyncSession = Depends(get_async_session)):
#     # cats = ["a2",
#     # "preposition",
#     # "pronoun",
#     # "b1",
#     # "conjunction",
#     # "verb",
#     # "modal verb",
#     # "b2",
#     # "determiner",
#     # "indefinite article",
#     # "definite article",
#     # "adjective",
#     # "a1",
#     # "number",
#     # "adverb",
#     # "linking verb",
#     # "noun",
#     # "ordinal number",
#     # "exclamation",
#     # "c1",]

#     cats = {
#         "anatomy": "Анатомия",
#         "animals": "Животные",
#         "appearance": "Внешность",
#         "archaeology": "Археология",
#         "architecture": "Архитектура",
#         "art": "Искусство",
#         "basic_verbs": "Базовые глаголы",
#         "business": "Бизнес",
#         "career": "Карьера",
#         "character": "Характер",
#         "clothing": "Одежда",
#         "colors": "Цвета",
#         "computer": "Компьютер",
#         "construction": "Строительство",
#         "ecology": "Экология",
#         "economy": "Экономика",
#         "family": "Семья",
#         "food": "Еда",
#         "furniture": "Мебель",
#         "geography": "География",
#         "health": "Здоровье",
#         "hobby": "Хобби",
#         "home": "Дом, вещи",
#         "idioms": "Идиомы",
#         "irregular_verbs": "Неправильные глаголы",
#         "legal_english": "Юриспруденция",
#         "literature": "Литература",
#         "marketing": "Маркетинг",
#         "mass_media": "СМИ",
#         "math": "Математика",
#         "military_weapons": "Военное дело, оружие",
#         "money": "Деньги",
#         "movie": "Кино",
#         "music": "Музыка",
#         "numbers": "Числительные (колич.)",
#         "numbers_ordinals": "Числительные (порядк.)",
#         "oxford3000_a1": "Oxford 3000 - A1",
#         "oxford3000_a2": "Oxford 3000 - A2",
#         "oxford3000_b1": "Oxford 3000 - B1",
#         "oxford3000_b2": "Oxford 3000 - B2",
#         "oxford5000_b2": "Oxford 5000 - B2",
#         "oxford5000_c1": "Oxford 5000 - C1",
#         "photography": "Фотография",
#         "phrasal_verbs": "Фразовые глаголы",
#         "politics": "Политика",
#         "psychology": "Психология",
#         "signs_of_zodiac": "Знаки зодиака",
#         "space": "Космос",
#         "sport": "Спорт",
#         "time": "Время",
#         "time_days_of_week": "Дни недели",
#         "time_months": "Месяцы",
#         "time_seasons": "Времена года",
#         "top100": "NGSL 1-100",
#         "top1000": "NGSL 101-1000",
#         "top3000": "NGSL 1001-3000",
#         "town": "Город",
#         "transport": "Транспорт",
#         "travel": "Путешествия",
#     }

#     for i in cats:
#         session.add(Category(name=i))  

#     await session.commit()

#     return 0