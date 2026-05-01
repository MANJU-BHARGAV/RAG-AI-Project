from backend.rag.pipeline import rag_pipeline

def qa_agent(query: str):
    return rag_pipeline(query)