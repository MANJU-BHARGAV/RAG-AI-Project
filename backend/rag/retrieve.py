__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb
from .embed import create_embedding

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)

def retrieve_documents(query):

    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    sources = []
    if metadatas and metadatas[0]:
        sources = [meta["source"] for meta in metadatas[0]]

    return documents, sources

