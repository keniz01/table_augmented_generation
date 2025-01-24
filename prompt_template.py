class PromptTemplate:

    _prompt_template="""
    <|system|>{system_prompt}<|end|>
    <|user|>
    Context:{context}
    Question: {question}<|end|>
    <|assistant|>"""
    
    @classmethod
    def from_template(cls, system_prompt:str, context:str, question:str) -> str:
        prompt=cls._prompt_template.format(system_prompt=system_prompt, context=context,question=question)
        return prompt