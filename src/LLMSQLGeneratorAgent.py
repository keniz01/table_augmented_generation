from os import path
from llama_cpp import Llama
from LLMSQLResponseFormatter import LLMSQLResponseFormatter

model_path=path.abspath(path.join(__file__ ,"../../.."))

class LLMSQLGeneratorAgent():
    def __init__(self):
        self.model = Llama(
            model_path=f"{model_path}//models/Phi-3.5-mini-instruct-Q6_K_L.gguf",
            n_ctx=2500,
            verbose=False,
            temperature=0    
        )
       
    def generate_sql(self, prompt:str):
        completion_response=self.model(prompt, max_tokens=2048)
        sql_text=completion_response["choices"][0]["text"]
        formatter=LLMSQLResponseFormatter(sql_text)
        return formatter.format_sql_response()
