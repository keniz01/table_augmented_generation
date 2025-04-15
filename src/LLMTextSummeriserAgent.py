from os import path
from llama_cpp import Llama

model_path=path.abspath(path.join(__file__ ,"../../.."))

class LLMTextSummeriserAgent():
    def __init__(self):
        self.model = Llama(
            model_path=f"{model_path}//models/Phi-3.5-mini-instruct-Q6_K_L.gguf",
            n_ctx=2500,
            verbose=False,
            temperature=0    
        )

    def summerise_text(self, prompt:str):
        completion_response=self.model(prompt, max_tokens=2048)
        summerised_text=completion_response["choices"][0]["text"]
        return summerised_text
