from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

category_word_table = Table(
    "category_word",
    Base.metadata,
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    Column("word_id", Integer, ForeignKey("words.id"), primary_key=True),
)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=True)
    sort_order = Column(Integer, default=0)

    words = relationship("Word", secondary=category_word_table, back_populates="categories")
    translations = relationship("CategoryTranslation", back_populates="category")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.owner_id or 'system'}"

    def __repr__(self):
        return f"{self.id} - {self.name}"


class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False) 
    name = Column(String, nullable=False)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, nullable=True)
    transcription = Column(Text, nullable=False)

    translations = relationship("WordTranslation", back_populates="word", cascade="all, delete-orphan")
    examples = relationship("Example", back_populates="word", cascade="all, delete-orphan")
    categories = relationship("Category", secondary=category_word_table, back_populates="words")


class WordTranslation(Base):
    __tablename__ = "word_translations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    text = Column(String, nullable=False)

    word = relationship("Word", back_populates="translations")
    language = relationship("Language")


class Example(Base):
    __tablename__ = "examples"
    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    word = relationship("Word", back_populates="examples")
    translations = relationship("ExampleTranslation", back_populates="example", cascade="all, delete-orphan")


class ExampleTranslation(Base):
    __tablename__ = "example_translations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    example_id = Column(Integer, ForeignKey("examples.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    text = Column(Text, nullable=False)

    example = relationship("Example", back_populates="translations")
    language = relationship("Language")


class CategoryTranslation(Base):
    __tablename__ = "category_translations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    name = Column(String, nullable=False)

    category = relationship("Category", back_populates="translations")
    language = relationship("Language")
