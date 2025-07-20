from pydantic import BaseModel


class LanguageCreate(BaseModel):
    code: str
    name: str
