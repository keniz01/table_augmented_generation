from os import path
import re
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama

model_path=path.abspath(path.join(__file__ ,"../../.."))

class EmbeddingModel():    
    def __init__(self):
        self.__embed_model=Llama(
            model_path=f"{model_path}/models/bge-small-en-v1.5-q4_k_m.gguf",
            embedding=True,
            verbose=False,
            pooling_type=LLAMA_POOLING_TYPE_LAST
        )
        
    def embed(self, content):
        vector=self.__embed_model.embed(content, normalize=True)
        return vector
    
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
    
class SQLResponseFormatter():

    def __init__(self, sql_response: str):
        self.sql_response=sql_response

    def remove_spaces(self):
        self.sql_response=self.sql_response.strip()
        return self

    def remove_back_ticks(self):
        self.sql_response=self.sql_response.replace('```sql','').replace('```','')
        return self
    
    def remove_wild_cards(self):
        self.sql_response=self.sql_response.replace("%",'')
        return self
    
    def replace_equals_with_ilike(self):
        pattern = r"=\s*'([^']*)'"
        self.sql_response = re.sub(pattern, r" ILIKE '\1'", self.sql_response)       
        return self
