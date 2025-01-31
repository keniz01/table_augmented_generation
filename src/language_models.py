from os import path
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
            n_ctx=2048,
            verbose=False,
            n_gpu_layers=0,
            logits_all=True,
            chat_format="chatml",
            temperature=0    
        )
    
    def generate_response(self, prompt:str):
        completion_response=self.model(prompt, max_tokens=2048)
        sql_response=completion_response["choices"][0]["text"].strip().replace('```sql','').replace('```','')
        return sql_response