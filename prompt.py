from abc import ABC, abstractmethod

class Prompt(ABC):

    @abstractmethod
    def generate_response() -> str:
        pass