from pathlib import Path

from llama_index.node_parser.text import SentenceSplitter
from llama_index.schema import TextNode

from chat_doc.config import BASE_DIR, logger


class DocumentProcessor:
    def __init__(self, loader, text_parser=SentenceSplitter(chunk_size=1024)):
        self.loader = loader
        self.text_parser = text_parser

    def load_documents(self, file_path):
        return self.loader.load_data(file=Path(file_path))

    def process_documents(self, documents=None):
        if not documents:
            documents = self.load_documents(file_path=Path(BASE_DIR + "/data/icd11.csv"))

        text_chunks = []
        doc_idxs = []
        for doc_idx, doc in enumerate(documents):
            cur_text_chunks = self.text_parser.split_text(doc.text)
            text_chunks.extend(cur_text_chunks)
            doc_idxs.extend([doc_idx] * len(cur_text_chunks))

        nodes = []
        for idx, text_chunk in enumerate(text_chunks):
            node = TextNode(text=text_chunk)
            src_doc = documents[doc_idxs[idx]]
            node.metadata = src_doc.metadata
            nodes.append(node)

        self.nodes = nodes
        return nodes
