from src.prompts.prompt_abstract import PromptAbstract

class TextSummariserPrompt(PromptAbstract):

    def __init__(self):
        super().__init__()

    def generate_prompt(self, context: str, question: str) -> str:
        
        prompt=f"""<|system|>You are a concise assistant. Respond only with the summarized result based strictly on the given context.<|end|>
<|user|>{question}<|end|>
<|assistant|>
Context: {context}
<|end|>
<|user|>Assume the question always matches the context. Your task is to summarize the value(s) from the context without explanation or reasoning.<|end|>
<|assistant|>"""

        return prompt