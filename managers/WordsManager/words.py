from sqlalchemy.ext.asyncio import AsyncSession
from models import Word, Category, Example, WordTranslation, category_word_table
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from typing import List
from schemas import words as words_schemas
from managers.CategoriesManager import CategoriesManager
from managers.LangManager import LangManager
from managers.ExamplesManager import ExamplesManager
from brokers.broker import broker
from starlette.responses import JSONResponse
from fastapi import HTTPException

cat_manager = CategoriesManager()
lang_manager = LangManager()
examples_manager = ExamplesManager()


class WordsManager:

    def __init__(self): ...

    async def get_all(self, session: AsyncSession):
        db_response = await session.execute(select(Word))
        return db_response.scalars().all()

    async def get_ids(self, session: AsyncSession):
        db_response = await session.execute(select(Word.id))
        return [i for i in db_response.scalars().all()]

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

    async def add_categories(self, session: AsyncSession, word: Word, cats: List[int]):
        new_values = [{"category_id": cat, "word_id": word.id} for cat in cats]
        stmt = (
            insert(category_word_table)
            .values(new_values)
            .returning(category_word_table)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def add_translations(
        self,
        session: AsyncSession,
        word: Word,
        translations: List[words_schemas.WordTranslationInput],
    ):
        lang_mapping = await lang_manager.get_mapping(session)
        new_values = [
            {
                "word_id": word.id,
                "language_id": lang_mapping[trans.lang],
                "text": trans.text,
            }
            for trans in translations
        ]
        stmt = insert(WordTranslation).values(new_values).returning(WordTranslation)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def check_categories_permissions(
        self, session: AsyncSession, data: words_schemas.WordsFullCreate
    ):
        cats = set()
        for word in data.words:
            for cat in word.categories:
                cats.add(cat)
        return await cat_manager.check_permissions(session, data.owner_id, cats)

    async def full_create(
        self, session: AsyncSession, data: words_schemas.WordsFullCreate
    ):
        if not await self.check_categories_permissions(session, data):
            raise HTTPException(403, "not permitted")
        new_words = []

        for word in data.words:
            stmt = (
                insert(Word)
                .values(
                    {"transcription": word.transcription, "owner_id": data.owner_id}
                )
                .returning(Word)
            )
            new_word = (await session.execute(stmt)).scalar_one()

            await self.add_categories(session, new_word, word.categories)
            await self.add_translations(session, new_word, word.translations)
            await examples_manager.create_examples(session, new_word.id, word.examples)

            new_words.append(new_word)

        await session.commit()

        # for i, word in enumerate(new_words):
        #     await broker.safe_publish(
        #         {
        #             "entity_type": "words",
        #             "id": word.id,
        #             "groups": data.words[i].categories,
        #         },
        #         "new_instances_queue",
        #     )

        return new_words
