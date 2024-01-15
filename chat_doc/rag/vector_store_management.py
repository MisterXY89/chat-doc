import psycopg2
from llama_index.vector_stores import PGVectorStore


class VectorStoreManager:
    def __init__(self, db_name, host, user, password, port, reset=False):
        self.db_name = db_name
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.vector_store = None
        self.reset = reset

    def setup_database(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            host=self.host,
            password=self.password,
            port=self.port,
            user=self.user,
        )
        self.conn.autocommit = True
        if self.reset:
            with self.conn.cursor() as c:
                c.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
                c.execute(f"CREATE DATABASE {self.db_name}")
            self.conn.close()

    def create_vector_store(self, table_name, embed_dim):
        self.vector_store = PGVectorStore.from_params(
            database=self.db_name,
            host=self.host,
            password=self.password,
            port=self.port,
            user=self.user,
            table_name=table_name,
            embed_dim=embed_dim,
        )

    def add_nodes(self, nodes):
        if self.vector_store:
            self.vector_store.add(nodes)
        else:
            raise Exception("Vector store not initialized.")
