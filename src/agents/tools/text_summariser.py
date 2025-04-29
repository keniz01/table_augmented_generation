from llama_cpp import Llama

class TextSummariser:

    def __init__(self, llm_model: Llama):
        self.__llm_model=llm_model

    def summarise_text(self, prompt:str):
        summerised_text=self.__llm_model.get_response(prompt)
        return summerised_text
