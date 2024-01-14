from llama_index import download_loader
from llama_index.query_engine import RetrieverQueryEngine
from tqdm import tqdm

from chat_doc.config import BASE_DIR
from chat_doc.rag.document_processing import DocumentProcessor
from chat_doc.rag.embedding_models import EmbeddingModel
from chat_doc.rag.llama_models import LlamaModel
from chat_doc.rag.retrieval import VectorDBRetriever
from chat_doc.rag.vector_store_management import VectorStoreManager


class RAGManager:
    def __init__(self):
        self.embed_model = None
        self.llama_model = None
        self.service_context = None
        self.vector_store_manager = None
        self.retriever = None
        self.query_engine = None
        self.init_rag()

    def init_rag(self):
        # Initialize embedding model
        self.embed_model = EmbeddingModel(model_name="BAAI/bge-small-en")

        # Initialize LLM model and service context
        self.llama_model = LlamaModel(
            model_url="https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf"
        )
        self.service_context = self.llama_model.create_service_context(self.embed_model.embed_model)

        # Initialize document processor and vector store manager
        SimpleCSVReader = download_loader("SimpleCSVReader")
        loader = SimpleCSVReader(encoding="utf-8")
        document_processor = DocumentProcessor(loader)

        self.vector_store_manager = VectorStoreManager(
            db_name="vector_db",
            host="localhost",
            user="docrag",
            password="rag-adl-llama",
            port="5432",
        )
        self.vector_store_manager.setup_database()
        self.vector_store_manager.create_vector_store(
            table_name="icd11",
            embed_dim=384,  # increase this to 768 if using a large model?
        )

        # if ADD_NODES (initialize vector store) is True, add nodes to vector store
        ADD_NODES = False
        if ADD_NODES:
            # TODO: Uncomment this to process documents for embeddings --> MAKE CLEANER (e.g. cli command)
            # Process documents for embeddings
            documents = document_processor.load_documents(BASE_DIR + "/data/icd11.csv")
            nodes = document_processor.process_documents(documents)
            self.vector_store_manager.add_nodes(nodes)

        # Initialize retriever and query engine
        self.retriever = VectorDBRetriever(
            self.vector_store_manager.vector_store,
            self.embed_model,
            # query_mode = "default"
            # query_mode = "sparse"
            # query_mode = "hybrid"
            query_mode="default",
            similarity_top_k=2,
        )
        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, service_context=self.service_context
        )

    def retrieve(self, query_string, use_llm=False):
        """
        Retrieve information based on the query string.

        Args:
            query_string (str): The query string for retrieval.
            use_llm (bool): Determines whether to use LLM for augmented generation or simple vector retrieval.

        Returns:
            Response from the retrieval process.
        """
        if use_llm:
            # Use LLM for augmented generation
            return self.query_engine.query(query_string)
        # Use simple passage retrieval from vector database
        return self.retriever.query(query_string)


def _handle_response(response):
    """
    Handle the response from the retrieval process.

    Args:
        response: The response from the retrieval process.
    """
    if isinstance(response, str):
        print(response)
    else:
        for node_with_score in response:
            print(f"Score: {node_with_score.score}, Content: {node_with_score.node.get_content()}")


def retrieve(query_string, use_llm=False):
    rag_manager = RAGManager()

    return _handle_response(rag_manager.retrieve(query_string, use_llm))


if __name__ == "__main__":
    # Example usage

    rag_manager = RAGManager()
    query_str = "What are the symptoms of a migraine?"
    print("Retrieving information based on the query string:")
    print(query_str + "\n")

    # Example usage with LLM
    print("Using LLM for augmented generation:")
    print(retrieve(query_str, use_llm=True))

    # Example usage with simple vector database retrieval
    print("\nUsing simple vector database retrieval:")
    print(retrieve(query_str))
