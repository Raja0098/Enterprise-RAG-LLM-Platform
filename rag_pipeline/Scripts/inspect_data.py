import os
from dotenv import load_dotenv
from pymilvus import connections, Collection

connections.connect(
                    "default",
                    host=os.getenv("MILVUS_HOST", "localhost"),
                    port=os.getenv("MILVUS_PORT", "19530")
                )
col = Collection("rag_docs")

print("Total entities:", col.num_entities)

col.load()

results = col.query(
    expr="id >= 0",
    output_fields=["text", "page", "source"],
    limit=3
)

print("Results:", results)