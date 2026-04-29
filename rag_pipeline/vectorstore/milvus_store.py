import os
from typing import List, Dict, Any

from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)


class MilvusStore:
    def __init__(
        self,
        collection_name: str = "rag_docs",
        dim: int = 384  # depends on your embedding model
    ):
        self.collection_name = collection_name
        self.dim = dim

        # 🔌 Connect to Milvus
        connections.connect(
            alias="default",
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )

        # 📦 Create or load collection
        if not utility.has_collection(self.collection_name):
            self._create_collection()

        self.collection = Collection(self.collection_name)

    # =========================
    # 📦 Create collection
    # =========================
    def _create_collection(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="page", dtype=DataType.INT64),
        ]

        schema = CollectionSchema(fields, description="RAG document store")

        collection = Collection(
            name=self.collection_name,
            schema=schema
        )

        # ⚡ Create index
        index_params = {
            "metric_type": "L2",  # or "IP" for cosine similarity
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }

        collection.create_index(
            field_name="embedding",
            index_params=index_params
        )

        print(f"✅ Created collection: {self.collection_name}")

    # =========================
    # 📥 Insert documents
    # =========================
    def insert(self, docs: List[Dict[str, Any]]):
        """
        docs format:
        [
            {
                "embedding": [...],
                "text": "some text",
                "source": "file.pdf",
                "page": 1
            }
        ]
        """

        embeddings = [d["embedding"] for d in docs]
        texts = [d["text"] for d in docs]
        sources = [d.get("source", "") for d in docs]
        pages = [d.get("page", 0) for d in docs]

        data = [
            embeddings,
            texts,
            sources,
            pages
        ]

        self.collection.insert(data)
        self.collection.flush()

        print(f"✅ Inserted {len(docs)} documents")

    # =========================
    # 🔍 Search
    # =========================
    def search(self, query_embedding: List[float], top_k: int = 3):
        self.collection.load()

        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10}
        }

        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["text", "source", "page"]
        )

        output = []
        for hits in results:
            for hit in hits:
                output.append({
                    "score": hit.score,
                    "text": hit.entity.get("text"),
                    "source": hit.entity.get("source"),
                    "page": hit.entity.get("page"),
                })

        return output

    # =========================
    # ❌ Delete collection
    # =========================
    def drop(self):
        utility.drop_collection(self.collection_name)
        print(f"🗑️ Dropped collection: {self.collection_name}")