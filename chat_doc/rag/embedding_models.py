from llama_index.embeddings import HuggingFaceEmbedding


class EmbeddingModel:
    def __init__(self, model_name):
        self.embed_model = HuggingFaceEmbedding(model_name=model_name)

    def get_text_embedding(self, text):
        return self.embed_model.get_text_embedding(text)

    def get_query_embedding(self, query):
        return self.embed_model.get_query_embedding(query)
