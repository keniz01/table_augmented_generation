class PromptTemplate:

    _prompt_template="""<|system|>{instructions}<|end|>
<|user|>
{context}
Question: {question}<|end|>
<|assistant|>"""
    
    @classmethod
    def from_template(cls, instructions:str, context:str, question:str) -> str:
        prompt=cls._prompt_template.format(instructions=instructions, context=context,question=question)
        return prompt