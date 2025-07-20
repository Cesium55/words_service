from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.words import ExampleInput, ExampleTranslationInput
from typing import List
from managers.LangManager import LangManager
from models import Example, ExampleTranslation
from managers.Logger import AsyncLogger

logger = AsyncLogger()

lang_manager = LangManager()


class ExamplesManager:

    async def create_example_translations(
        self,
        session: AsyncSession,
        example_id: int,
        translations: List[ExampleTranslationInput],
    ):
        lang_mapping = await lang_manager.get_mapping(session)

        new_values = [
            {
                "language_id": lang_mapping[trans.lang],
                "example_id": example_id,
                "text": trans.text,
            }
            for trans in translations
        ]

        stmt = (
            insert(ExampleTranslation).values(new_values).returning(ExampleTranslation)
        )
        new_translations = await session.execute(stmt)
        return new_translations.scalars().all()

    async def create_example(
        self,
        session: AsyncSession,
        word_id: int,
        example: List[ExampleTranslationInput],
    ):
        stmt = insert(Example).values({"word_id": word_id}).returning(Example)
        new_example = (await session.execute(stmt)).scalar_one()

        await self.create_example_translations(session, new_example.id, example)

        return new_example

    async def create_examples(
        self,
        session: AsyncSession,
        word_id: int,
        examples: List[List[ExampleTranslationInput]],
    ):
        new_examples = []

        for example in examples:
            new_examples.append(await self.create_example(session, word_id, example))

        return new_examples
