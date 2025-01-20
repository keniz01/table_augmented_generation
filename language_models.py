from llama_cpp import LLAMA_POOLING_TYPE_LAST, Llama

class EmbeddingModel():
    
    def __init__(self):
        self.embed_model=Llama(
            model_path='../models/bge-small-en-v1.5-q4_k_m.gguf',
            embedding=True,
            verbose=False,
            pooling_type=LLAMA_POOLING_TYPE_LAST
        )