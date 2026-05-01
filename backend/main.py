# 🔥 Fix sqlite issue (MUST BE FIRST)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# -------------------------------
# Imports
# -------------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List
import os
import chromadb

from backend.agents.orchestrator import route_query
from backend.rag.ingest import ingest_document

# -------------------------------
# App Initialization
# -------------------------------
app = FastAPI(
    title="Multi-Agent AI RAG System",
    description="Upload documents and query using RAG + Multi-Agent system",
    version="2.0"
)

# -------------------------------
# ChromaDB Client (for reset API)
# -------------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="knowledge_base")

# -------------------------------
# Upload Directory
# -------------------------------
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------
# Templates (UI)
# -------------------------------
templates = Jinja2Templates(directory="backend/templates")

# -------------------------------
# Request Model
# -------------------------------
class QueryRequest(BaseModel):
    query: str

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def root():
    return {"message": "🚀 AI Multi-Agent RAG API is running"}

# -------------------------------
# ✅ Single Upload Endpoint (MULTIPLE FILES)
# -------------------------------
@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        uploaded_files = []

        for file in files:
            # 🔒 Validate file type
            if not file.filename.endswith((".txt", ".pdf")):
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} not supported. Only .txt and .pdf allowed"
                )

            file_path = os.path.join(UPLOAD_DIR, file.filename)

            # Save file
            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Ingest into vector DB
            ingest_document(file_path)

            uploaded_files.append(file.filename)

        return {
            "message": f"{len(uploaded_files)} file(s) uploaded and indexed successfully",
            "files": uploaded_files
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)  # 🔥 debug
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# Query Endpoint
# -------------------------------
@app.post("/query")
def query(request: QueryRequest):
    try:
        result = route_query(request.query)
        return result

    except Exception as e:
        print("QUERY ERROR:", e)  # 🔥 debug
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# Clear Database
# -------------------------------
@app.delete("/clear-db")
def clear_db():
    try:
        collection.delete(where={})
        return {"message": "🧹 Vector database cleared successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------
# UI Endpoint
# -------------------------------
@app.get("/ui", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})