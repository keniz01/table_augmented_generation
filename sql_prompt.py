from language_models import InstructionModel
from prompt import Prompt
from prompt_template import PromptTemplate
from database_context_retriever import DatabaseContextRetriever
      
class SqlPrompt(Prompt):

    def __init__(self):
        super().__init__()

    def generate_response(self, question: str) -> str:
        
        instructions=f"""You are a PostgreSQL expert. Generate correct a correct SQL statement from the context information provided to answer the question at the end.
        You must use only the column names provided in the context, don't make up column names. If you can't find an answer, say you dont know.
        Do not wrap the response in any backticks (```) or anything else. Respond with a valid SQL statement only.
        Do not return comments, assumptions or sequence of steps.
        Adhere to these rules:
        - Use ILIKE when comparing case sensitive strings instead of the equal (=) operator.
        - Always use table and columns aliases.
        - No INSERT, UPDATE, DELETE instructions, CREATE, ALTER or DROP instructions."""

        context=DatabaseContextRetriever.from_question(question=question)
        prompt=PromptTemplate.from_template(instructions=instructions, context=context, question=question)
        instruction_model=InstructionModel()
        sql_statement=instruction_model.generate_response(prompt=prompt)

        return sql_statement

sql_prompt=SqlPrompt()
question="Can you show all album titles by artist Capleton release on label Jet Star?"
sql_statement=sql_prompt.generate_response(question=question)
print(sql_statement)