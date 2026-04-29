from fastapi import APIRouter, UploadFile, HTTPException
import shutil
import uuid
from datetime import datetime

from pipelines.ingestion_pipeline import ingest
from pipelines.rag_pipeline import RAGPipeline
from config.db import get_connection

router = APIRouter(tags=["RAG"])
rag_pipeline = RAGPipeline()

# ---------------------------
# Upload & Ingest
# ---------------------------
@router.post("/upload/")
async def upload(file: UploadFile):
    path = f"docs/{file.filename}"
    try:
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger your ML ingestion pipeline
        ingest(path)
        return {"status": "ingested", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Query (RAG)
# ---------------------------
@router.post("/query")
def query(data: dict):
    question = data.get("question")
    session_id = data.get("session_id", "default")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        result = rag_pipeline.ask(question, session_id)
        
        # Standardized response format for the Vue frontend
        return {
            "response": result.get("answer", result) if isinstance(result, dict) else result,
            "summary": result.get("summary", "") if isinstance(result, dict) else "",
            "meta_data": result.get("citations", []) if isinstance(result, dict) else [],
            "table_data": result.get("table_data", []) if isinstance(result, dict) else [],
            "follow_up": result.get("follow_up", []) if isinstance(result, dict) else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Message Management
# ---------------------------
@router.post("/chat/message")
def save_message(data: dict):
    session_id = data.get("session_id")
    role = data.get("role")
    content = data.get("response") # Mapping to 'response' as sent by Vuex store

    if not session_id or not role or not content:
        raise HTTPException(status_code=400, detail="Missing required fields")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO chat_memory (session_id, role, content, created_at)
            VALUES (%s, %s, %s, %s)
        """, (session_id, role, content, datetime.utcnow()))
        conn.commit()
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# ---------------------------
# Session Management
# ---------------------------
@router.post("/chat/session")
def create_session(data: dict):
    session_id = str(uuid.uuid4())
    return {"session_id": session_id, "title": data.get("title", "New Chat")}

@router.get("/sessions")
def get_sessions():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Get unique sessions with their last message time
        cur.execute("""
            SELECT session_id, MAX(created_at) as last_active 
            FROM chat_memory 
            GROUP BY session_id 
            ORDER BY last_active DESC
        """)
        return [{"session_id": r[0], "title": f"Chat {r[0][:8]}"} for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

@router.get("/sessions/{session_id}/chats")
def get_chats(session_id: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT role, content, created_at
            FROM chat_memory
            WHERE session_id = %s
            ORDER BY created_at ASC
        """, (session_id,))
        rows = cur.fetchall()
        return {
            "session_id": session_id,
            "chats": [{"role": r[0], "message": r[1], "time": str(r[2])} for r in rows]
        }
    finally:
        cur.close()
        conn.close()

# ---------------------------
# ADMIN ANALYTICS (For the Charts)
# ---------------------------
@router.get("/admin/stats")
def get_admin_stats():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Gets query counts per day for the Bar Chart
        cur.execute("""
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') as date, COUNT(*) 
            FROM chat_memory 
            WHERE role = 'user'
            GROUP BY date 
            ORDER BY date ASC
            LIMIT 7
        """)
        rows = cur.fetchall()
        return [{"date": r[0], "count": r[1]} for r in rows]
    finally:
        cur.close()
        conn.close()