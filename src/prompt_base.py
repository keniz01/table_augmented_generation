from abc import ABC, abstractmethod

class AbstractPrompt(ABC):
    @abstractmethod
    def generate_prompt(self, context: str, question: str) -> str:
        pass