from prompt_template import PromptTemplate
from prompt_base import AbstractPrompt

class SummarizerPrompt(AbstractPrompt):

    def generate_prompt(self, context: str, question: str) -> str:
        
        prompt=f"""<|system|>You are a helpful assistant.<|end|>
<|user|>{question}<|end|>
<|assistant|>
Context: {context}
<|end|>
<|user|>You must summarize the values in the context regardless of the question.<|end|>
<|assistant|>"""

        # prompt=PromptTemplate.from_template(instructions=instructions, context=context, question=question)
        return prompt