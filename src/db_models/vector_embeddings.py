from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class VectorEmbeddings(Base):
    __tablename__ = 'vector_embeddings'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    raw_json = Column(JSONB, nullable=False)
    embeddings = Column(Vector(384), nullable=False)