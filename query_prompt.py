import os
import textwrap
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama
import psycopg
from sqlalchemy import create_engine, select, text
import pandas as pd
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base
from database_models import DatabaseMetaData
from language_models import EmbeddingModel, InstructionModel
from prompt_template import PromptTemplate
from database_context_retriever import DatabaseContextRetriever
 
user_query="Can you show all album titles by artist Capleton release on label Jet Star?"

system_prompt=f"""You are a PostgreSQL expert. Generate correct a correct SQL statement from the context information provided to answer the question at the end.
You must use only the column names provided in the context, don't make up column names. If you can't find an answer, say you dont know.
Do not wrap the response in any backticks (```) or anything else. Respond with a valid SQL statement only.
Do not return comments, assumptions or sequence of steps.
Adhere to these rules:
- Use ILIKE when comparing case sensitive strings instead of the equal (=) operator.
- Always use table and columns aliases.
- No INSERT, UPDATE, DELETE instructions, CREATE, ALTER or DROP instructions."""

context=DatabaseContextRetriever.from_question(user_query)
prompt=PromptTemplate.from_template(system_prompt=system_prompt, context=context, question=user_query)
instruction_model=InstructionModel()
sql_query=instruction_model.generate_response(prompt=prompt)
print(sql_query)