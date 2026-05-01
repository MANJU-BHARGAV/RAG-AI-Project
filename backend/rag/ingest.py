__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import PyPDF2
import uuid
import os
import chromadb
from backend.rag.embed import create_embedding

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)

DATA_PATH = "data/documents"

# 🔥 NEW: simple chunking function
def split_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap

    return chunks

def load_document(file_path):
    # TXT
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # PDF
    elif file_path.endswith(".pdf"):
        text = ""

        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()

        return text

    else:
        raise ValueError("Unsupported file type")

def ingest_document(file_path):
    import uuid

    text = load_document(file_path)

    chunks = split_text(text)

    for chunk in chunks:
        embedding = create_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": file_path}],
            ids=[str(uuid.uuid4())]
        )

    print(f"✅ Ingested {file_path}")


if __name__ == "__main__":
    import os

    folder = "data/documents"

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        if file.endswith((".txt", ".pdf")):
            ingest_document(file_path)