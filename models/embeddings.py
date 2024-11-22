from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.model = SentenceTransformer(model_name)

    def encode_text(self, text):
        if not text:
            raise ValueError("Input text cannot be empty")
        return self.model.encode(text)
    