from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
Base = declarative_base()

class DatabaseMetaData(Base):
    __tablename__ = 'database_meta_data'

    table_schema_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    table_name = Column(String(255), nullable=False)
    table_description = Column(String(255), nullable=False)
    table_json_schema = Column(JSONB, nullable=False)
    vector_embeddings = Column(Vector(384), nullable=False)