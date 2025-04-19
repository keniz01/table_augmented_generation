from os import path
from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama

class TextEmbeddingModel(): 
       
    def __init__(self):
        model_path=path.abspath(path.join(__file__ ,"../../../.."))
        self.__embed_model=Llama(
            model_path=f"{model_path}/models/bge-small-en-v1.5-q4_k_m.gguf",
            embedding=True,
            verbose=False,
            pooling_type=LLAMA_POOLING_TYPE_LAST
        )
        
    def embed_text(self, content: str):
        vector=self.__embed_model.embed(content, normalize=True)
        return vector
