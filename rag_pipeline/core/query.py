from vectorstore.milvus_store import MilvusStore
from core.gemini_client import client
from google.genai import types
from conversation.memory import PostgresMemory 
import re
import hashlib
from sentence_transformers import CrossEncoder
 

class RAGQuery:
    def __init__(self):
        self.store = MilvusStore()
        self.memory = PostgresMemory()
        self.reranker = CrossEncoder("BAAI/bge-reranker-base")

    # =========================
    # 🔹 INTENT CLASSIFIER (NEW)
    # =========================
    def classify_query(self, query):
        prompt = f"""
Classify the query into one of:

1. COMPANY
2. GENERAL

Query: {query}

Output only one word.
"""
        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return res.text.strip().upper()
        except:
            return "COMPANY"


    # =========================
    # 🔹 GENERAL ANSWER (NEW)
    # =========================
    def answer_general(self, query, history_text):
        prompt = f"""
You are a helpful assistant.

Answer the question naturally.

[CONVERSATION HISTORY]
{history_text if history_text else "NONE"}

[QUESTION]
{query}
"""
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "answer": res.text.strip(),
            "summary": res.text.strip()[:150],
            "follow_up": [],
            "citations": [],
            "chunks_used": 0,
            "queries_used": [query],
            "session_id": "general"
        }


    # =========================
    # 🔹 EMBEDDING
    # =========================
    def get_embedding(self, text: str):
        res = client.models.embed_content(
            model="gemini-embedding-2-preview",
            contents=[text],
            config=types.EmbedContentConfig(output_dimensionality=768)
        )
        return res.embeddings[0].values


    # =========================
    # 🔹 QUERY EXPANSION (TWEAKED)
    # =========================
    def generate_queries(self, query, history_text):
        if len(query.split()) > 6:
            return [query]

        prompt = f"""  # (UNCHANGED PROMPT)
{query}
{history_text}
"""

        try:
            res = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            queries = [q.strip() for q in res.text.strip().split("\n") if q.strip()]

            # 🔥 CHANGE: allow up to 4 queries
            return list(set([query] + queries))[:4]

        except:
            return [query]


    # =========================
    # 🔹 RERANK (IMPROVED)
    # =========================
    def rerank(self, queries, docs, top_k=3):
        if not docs:
            return []

        def truncate(text, max_len=512):
            return text[:max_len]

        all_pairs = []
        doc_map = []

        # 🔥 MULTI-QUERY RERANK
        for i, d in enumerate(docs):
            for q in queries:
                all_pairs.append((q, truncate(d.get("text", ""))))
                doc_map.append(i)

        scores = self.reranker.predict(all_pairs)

        # max score per doc
        doc_scores = {}
        for idx, score in zip(doc_map, scores):
            doc_scores[idx] = max(doc_scores.get(idx, -999), score)

        ranked = sorted(
            [(docs[i], s) for i, s in doc_scores.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, _ in ranked[:top_k]]


    # =========================
    # 🔹 MAIN PIPELINE
    # =========================
    def ask(self, q: str, session_id: str = "default"):

        # -------- HISTORY --------
        history = self.memory.get_history(session_id, limit=6)

        history_text = "\n".join([
            f"{h['role']}: {h['content']}" for h in history
        ]) if history else ""

        # -------- INTENT --------
        intent = self.classify_query(q)

        if intent == "GENERAL":
            return self.answer_general(q, history_text)

        # -------- QUERY EXPANSION --------
        queries = self.generate_queries(q, history_text)

        print("\n🔍 Queries:", queries)

        # -------- RETRIEVAL --------
        all_docs = []

        for query in queries:
            emb = self.get_embedding(query)
            docs = self.store.search(emb, top_k=5)

            for d in docs:
                d["query_used"] = query
                all_docs.append(d)

        # -------- DEDUP (IMPROVED) --------
        seen = set()
        unique_docs = []

        for d in all_docs:
            text = d.get("text", "")
            key = hashlib.md5(text.encode()).hexdigest()

            if key not in seen:
                seen.add(key)
                unique_docs.append(d)

        print(f"\n📄 Retrieved {len(unique_docs)} docs")

        # 🔥 EARLY FALLBACK
        if len(unique_docs) == 0:
            return self.answer_general(q, history_text)

        # -------- RERANK --------
        docs = self.rerank(queries, unique_docs)

        # -------- CONTEXT BUILD --------
        context_parts = []
        citations = []

        for d in docs:
            text = d.get("text", "")[:500]

            context_parts.append(f"""
[CHUNK]
{text}

[METADATA]
source: {d.get("source")}
page: {d.get("page")}
""")

            citations.append({
                "source": d.get("source"),
                "page": d.get("page"),
                "url": d.get("url")
            })

        context = "\n\n".join(context_parts)

        # -------- PROMPT (UNCHANGED) --------
        prompt = f"""  # your original prompt unchanged
{context}
{history_text}
{q}
"""

        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_answer = res.text.strip()

        # ---------------- PARSE SAME ----------------
        sections = {"answer": "", "summary": "", "followups": []}
        current = None

        for line in raw_answer.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith("answer:"):
                current = "answer"
                continue
            elif line.lower().startswith("summary:"):
                current = "summary"
                continue
            elif "follow-up" in line.lower():
                current = "followups"
                continue

            if current == "answer":
                sections["answer"] += line + "\n"
            elif current == "summary":
                sections["summary"] += line + "\n"
            elif current == "followups":
                clean = line.lstrip("*-0123456789. ").strip()
                if clean:
                    sections["followups"].append(clean)

        answer = sections["answer"].strip()
        summary = sections["summary"].strip()
        followups = sections["followups"][:1]

        if not summary:
            summary = answer[:150]

        # -------- MEMORY --------
        self.memory.add_turn(session_id, "user", q)
        self.memory.add_turn(session_id, "assistant", answer)

        return {
            "answer": answer,
            "summary": summary,
            "follow_up": followups,
            "citations": citations[:2],
            "chunks_used": len(docs),
            "queries_used": queries,
            "session_id": session_id
        }