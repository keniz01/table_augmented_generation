from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase):
    pass

class DatabaseMetaData(Base):
    __tablename__ = 'database_meta_data'

    table_schema_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    table_name = Column(String(255), nullable=False)
    table_description = Column(String(255), nullable=False)
    table_meta_data = Column(JSONB, nullable=False)
    vector_embeddings = Column(Vector(384), nullable=False)