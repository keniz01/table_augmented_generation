from language_models import InstructionModel
from prompt_template import PromptTemplate

class ResponseSynthesizePrompt:

    def generate_response(self, context: str, question: str) -> str:
        
        instructions="""You are a smart chatbot. 
You must the context provided to answer the question. 
The response must not include any advice, comments, assumptions or sequence of steps.
If you dont know the answer, say you dont know."""

        prompt=PromptTemplate.from_template(instructions=instructions, context=context, question=question)
        instruction_model=InstructionModel()
        sql_statement=instruction_model.generate_response(prompt=prompt)
        return sql_statement