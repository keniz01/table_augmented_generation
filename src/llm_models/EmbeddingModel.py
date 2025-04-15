from os import path
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama

model_path=path.abspath(path.join(__file__ ,"../../../.."))

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
