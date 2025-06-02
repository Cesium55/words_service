from sqlalchemy import Column, Integer, String, create_engine, Boolean, DateTime, ForeignKey, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func


Base = declarative_base()

# word_category_association = Table(
#     'word_category_association', Base.metadata,
#     Column('word_id', Integer, ForeignKey('words.id'), primary_key=True),
#     Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
# )



# class Word(Base):
#     __tablename__ = "words"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     transcription = Column(String, nullable=True)
#     owner_id = Column(Integer, nullable=True)

#     translations = relationship("WordTranslation", back_populates="word", cascade="all, delete-orphan")
#     categories = relationship('Category', secondary=word_category_association, back_populates='words')
#     examples = relationship("Example", back_populates="word")

# class WordTranslation(Base):
#     __tablename__ = "word_translations"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"))
#     language = Column(String, nullable=False)  # e.g., 'en', 'ru', 'fr'
#     text = Column(String, nullable=False)

#     word = relationship("Word", back_populates="translations")

    
    


# class Example(Base):
#     __tablename__ = "examples"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     owner_id = Column(Integer, nullable=True)

#     word_id = Column(Integer, ForeignKey("words.id", ondelete='CASCADE'))
#     word = relationship("Word", back_populates="examples")
    
#     translations = relationship("ExampleTranslation", back_populates="example", cascade="all, delete-orphan")

    
#     def __str__(self):
#         return self.english
    
#     def __repr__(self):
#         return self.english

# class ExampleTranslation(Base):
#     __tablename__ = "example_translations"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     example_id = Column(Integer, ForeignKey("examples.id", ondelete="CASCADE"))
#     language = Column(String, nullable=False)
#     text = Column(String, nullable=False)

#     example = relationship("Example", back_populates="translations")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=True)
    
    sort_order = Column(Integer, default=0)
    
    # words = relationship('Word', secondary=word_category_association, back_populates='categories')
    
    
    def __str__(self):
        return f"{self.id} - {self.name} - {self.owner_id or 'system'}"
    
    def __repr___(self):
        return f"{self.id} - {self.name}"

