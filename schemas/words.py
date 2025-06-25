from pydantic import BaseModel, model_validator
from typing import List, Dict, Optional, Any

class ExampleTranslationInput(BaseModel):
    language_code: str  # код языка (например 'eng', 'rus')
    text: str

class ExampleInput(BaseModel):
    translations: List[ExampleTranslationInput]

class WordTranslationInput(BaseModel):
    language_code: str  # код языка (например 'eng', 'rus')
    text: str

class WordInput(BaseModel):
    translations: List[WordTranslationInput]
    examples: List[ExampleInput] = []
    categories: List[str] = []
    transcription: str

class WordsImportRequest(BaseModel):
    words: List[WordInput]
    owner_id: int | None = None

class WordsByIDs(BaseModel):
    ids: List[int]



########################################
######### word return section ##########

class LanguageData(BaseModel):
    name: str
    code: str
    # id: int

class Translation(BaseModel):
    # id: int
    text: str
    language: LanguageData

class Category(BaseModel):
    owner_id: Optional[int]
    id: int
    name: str


class Example(BaseModel):
    # id: int
    translations: List[Translation]

class Word(BaseModel):
    id: int
    owner_id: object
    transcription: Optional[str]
    categories: List[Category]
    translations: List[Translation]
    examples: List[Example]

class WordsReturnSchema(BaseModel):
    data: List[Word]

########################################