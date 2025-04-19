from abc import ABC, abstractmethod

class PromptAbstract(ABC):
    @abstractmethod
    def generate_prompt(self, context: str, question: str) -> str:
        pass