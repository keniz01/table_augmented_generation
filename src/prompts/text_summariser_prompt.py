from src.prompts.prompt_abstract import PromptAbstract

class TextSummariserPrompt(PromptAbstract):

    def __init__(self):
        super().__init__()

    def generate_prompt(self, context: str, question: str) -> str:
        
        prompt=f"""<|system|>You are a helpful assistant.<|end|>
<|user|>{question}<|end|>
<|assistant|>
Context: {context}
<|end|>
<|user|>You must summarize the values in the context regardless of the question. Do not explain, advice or assume.<|end|>
<|assistant|>"""

        return prompt