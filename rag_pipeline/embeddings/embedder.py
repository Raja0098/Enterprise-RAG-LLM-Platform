from core.gemini_client import client
from google.genai import types


class Embedder:
    def embed(self, chunks):
        data = []

        for c in chunks:
            text = c.get("text", "").strip()

            # Skip empty text
            if not text:
                continue

            try:
                res = client.models.embed_content(
                    model="gemini-embedding-2-preview",   
                    contents=[text],
                    config=types.EmbedContentConfig(
                        output_dimensionality=768  
                    )               
                )

                embedding = res.embeddings[0].values  

                data.append({
                    "embedding": embedding,
                    "text": text,
                    "metadata": c["metadata"]
                })

            except Exception as e:
                print(f"Embedding failed: {e}")
                continue

        return data