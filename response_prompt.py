from language_models import InstructionModel
from prompt_template import PromptTemplate
from database_context_retriever import DatabaseContextRetriever
      
class ResponseSynthesizePrompt:

    def generate_response(self, context: str) -> str:
        
        instructions="""You are a summarizer chatbot. 
Summarise the context information given into a meaningful response to answer the question.
Do not return comments, assumptions or advice. If you dont know the answer,say you dont know."""

        prompt=PromptTemplate.from_template(instructions=instructions, context=context)
        instruction_model=InstructionModel()
        sql_statement=instruction_model.generate_response(prompt=prompt)
        return sql_statement