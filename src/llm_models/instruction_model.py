from os import path
from llama_cpp import Llama

class InstructionModel():    
    def __init__(self):

        model_path=path.abspath(path.join(__file__ ,"../../../.."))
        self.__llm_model = Llama(
            model_path=f"{model_path}//models/Phi-3.5-mini-instruct-Q6_K_L.gguf",
            n_ctx=2500,
            verbose=False,
            temperature=0,
            logits_all=False    
        )
    def get_response(self, prompt: str) -> str:
        completion_response=self.__llm_model(prompt, max_tokens=2048)
        response=completion_response["choices"][0]["text"]
        return response
