import os
from ingestion.loader import pdf_to_images
from ingestion.gemini_ocr import GeminiPipeline
from ingestion.chunker import smart_chunk
from embeddings.embedder import Embedder
from vectorstore.milvus_store import MilvusStore

BASE_URL = "http://localhost:8000/docs"

def ingest(pdf_path):
    source = os.path.basename(pdf_path)

    print("🔵 Using Gemini pipeline")

    images = pdf_to_images(pdf_path)
    gemini = GeminiPipeline()

    chunks, _ = gemini.run(images, source, BASE_URL)

    chunks = smart_chunk(chunks)

    embedder = Embedder()
    data = embedder.embed(chunks)

    store = MilvusStore()
    store.insert(data)

    print("✅ Ingestion complete")