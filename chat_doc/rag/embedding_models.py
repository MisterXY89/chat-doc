from llama_index.embeddings import HuggingFaceEmbedding
from tqdm import tqdm


class EmbeddingModel:
    def __init__(self, model_name):
        self.embed_model = HuggingFaceEmbedding(model_name=model_name)

    # redirect methods to embed_model
    def get_text_embedding(self, text):
        return self.embed_model.get_text_embedding(text)

    def get_query_embedding(self, query):
        return self.embed_model.get_query_embedding(query)

    def embed_nodes(self, nodes):
        for node in tqdm(nodes):
            node_embedding = self.embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
        return nodes
