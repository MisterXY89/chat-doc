from pathlib import Path

import pandas as pd
from llama_index import Document
from llama_index.node_parser.text import SentenceSplitter
from llama_index.schema import TextNode
from tqdm import tqdm

from chat_doc.config import BASE_DIR, logger


class DocumentProcessor:
    def __init__(self, loader, text_parser=SentenceSplitter()):
        self.loader = loader
        self.text_parser = text_parser

    def load_documents(self, file_path):
        return self.loader.load_data(file=Path(file_path))

    def process_documents(self, documents_df=None):
        if not documents_df:
            documents_df = pd.read_csv(Path(BASE_DIR + "/data/icd11.csv"))

        def build_node(row):
            node = TextNode(text=row["definition"])
            node.metadata = {
                "id": row["id"],
                "name": row["name"],
            }
            return node

        nodes = []

        for idx, row in tqdm(documents_df.iterrows(), total=len(documents_df)):
            nodes.append(build_node(row))

        # text_chunks = []
        # doc_idxs = []
        # for doc_idx, doc in enumerate(documents):
        #     cur_text_chunks = self.text_parser.split_text(doc.text)
        #     text_chunks.extend(cur_text_chunks)
        #     doc_idxs.extend([doc_idx] * len(cur_text_chunks))

        # nodes = self.text_parser.split_text(list(map(lambda d: d.text[0], documents)))

        # nodes = []
        # for raw_node in enumerate(nodes):
        #     node = TextNode(text=raw_node)
        #     # src_doc = documents[doc_idxs[idx]]
        #     # node.metadata = src_doc.metadata
        #     nodes.append(node)

        self.nodes = nodes
        return nodes
