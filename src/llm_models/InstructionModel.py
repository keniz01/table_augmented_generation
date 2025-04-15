from os import path
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama

model_path=path.abspath(path.join(__file__ ,"../../.."))

class InstructionModel():
    def __init__(self):
        self.model = Llama(
            model_path=f"{model_path}//models/Phi-3.5-mini-instruct-Q6_K_L.gguf",
            n_ctx=2500,
            verbose=False,
            temperature=0    
        )

    def generate_summary_response(self, prompt:str):
        completion_response=self.model(prompt, max_tokens=2048)
        response_text=completion_response["choices"][0]["text"]
        return response_text
       
    def generate_sql_response(self, prompt:str):
        completion_response=self.model(prompt, max_tokens=2048)
        sql_text=completion_response["choices"][0]["text"]
        formatter=SQLResponseFormatter(sql_text).remove_spaces().remove_back_ticks().remove_wild_cards().replace_equals_with_ilike()
        return formatter.sql_response
