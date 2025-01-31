from language_models import InstructionModel
from prompt import Prompt
from prompt_template import PromptTemplate
from database_context_retriever import DatabaseContextRetriever
      
class SqlPrompt(Prompt):

    def __init__(self):
        super().__init__()

    def generate_response(self, question: str) -> str:
        
        instructions="""You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most 15 results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Only return SQL response - the response must not include any advice, comments, assumptions or sequence of steps."""

        context=DatabaseContextRetriever.from_question(question=question)
        prompt=PromptTemplate.from_template(instructions=instructions, context=context, question=question)
        instruction_model=InstructionModel()
        sql_statement=instruction_model.generate_response(prompt=prompt)

        return sql_statement