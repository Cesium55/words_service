from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models import Language


class LangManager:

    async def get_mapping(self, session: AsyncSession) -> dict:
        """returns mapping {'code1': id1, 'code2': id2, ...}"""
        result = await session.execute(select(Language.id, Language.code))
        language_map = {code: id_ for id_, code in result.all()}
        return language_map
