from typing import Any, List, Optional

from llama_index import QueryBundle
from llama_index.retrievers import BaseRetriever
from llama_index.schema import NodeWithScore
from llama_index.vector_stores import VectorStoreQuery


class VectorDBRetriever(BaseRetriever):
    def __init__(self, vector_store, embed_model, query_mode="default", similarity_top_k=2):
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query_embedding = self._embed_model.get_query_embedding(query_bundle.query_str)
        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding,
            similarity_top_k=5,
            mode=self._query_mode,
        )

        query_result = self._vector_store.query(vector_store_query)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
                nodes_with_scores.append(NodeWithScore(node=node, score=score))

        return nodes_with_scores

    def query(self, query_str: str) -> Any:
        print("Querying...")
        # Check if embeddings exist for the nodes in the vector store.
        embeddings_exist = self._check_embeddings_existence()
        if not embeddings_exist:
            # Prompt the user to decide whether to process documents for embeddings.
            process_documents = self._ask_user_for_processing()
            if process_documents:
                self._process_documents()
            else:
                return "Embeddings are missing. Please process documents for embeddings."

        return self._retrieve(query_bundle=QueryBundle(query_str=query_str))

    def _check_embeddings_existence(self):
        """
        Check if embeddings exist for the nodes in the vector store.

        Returns:
            bool: True if embeddings exist, False otherwise.
        """
        # Implement the logic to check if embeddings exist.
        # This could be a database query or a check in the vector store.
        return True  # Placeholder return

    def _ask_user_for_processing(self):
        """
        Prompt the user to decide whether to process documents for embeddings.

        Returns:
            bool: True if user agrees to process, False otherwise.
        """
        user_input = (
            input(
                "Embeddings are missing. Would you like to start processing documents to generate embeddings? (y/n): "
            )
            .strip()
            .lower()
        )
        return user_input == "y"
