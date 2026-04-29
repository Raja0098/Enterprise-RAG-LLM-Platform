from pymilvus import connections, utility, Collection

connections.connect("default", host="localhost", port="19530")

print("Collections:", utility.list_collections())

col = Collection("rag_docs")

print("Total entities:", col.num_entities)

utility.drop_collection("rag_docs")
print("✅ Deleted old collection")