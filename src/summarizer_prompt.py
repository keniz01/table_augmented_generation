from prompt_template import PromptTemplate
from prompt_base import AbstractPrompt

class SummarizerPrompt(AbstractPrompt):

    def generate_prompt(self, context: str, question: str) -> str:
        
        instructions="""You are a helpful assistant. Please describe the table in the given context.
The response must fully or partially answer the question. Always assume the context has all the required information. 
You must not return any advice, comments, assumptions or sequence of steps.
If you dont know the answer, say you dont know."""

        prompt=PromptTemplate.from_template(instructions=instructions, context=context, question=question)
        return prompt