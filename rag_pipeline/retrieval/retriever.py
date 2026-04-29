from embeddings.embedder import Embedder
from vectorstore.milvus_store import MilvusStore


class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.store = MilvusStore()

    def retrieve(self, query: str, top_k=5):
        # 1️⃣ Convert query → embedding
        emb = self.embedder.embed_query(query)

        # 2️⃣ Search in Milvus
        results = self.store.search(emb, top_k)

        return results