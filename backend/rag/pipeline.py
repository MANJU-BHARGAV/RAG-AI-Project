from .retrieve import retrieve_documents
from backend.llm.llm_client import generate_response

def rag_pipeline(query):

    docs, sources = retrieve_documents(query)

    if not docs or not docs[0]:
        return {
            "response": "No relevant documents found ❌",
            "sources": []
        }

    context = "\n".join([doc for sublist in docs for doc in sublist])

    prompt = f"""
Answer the question using the context below.
You are allowed to infer meaning from the context.
Do not say "I don't know" unless the topic is completely unrelated.
Keep the answer short (2-3 sentences).

Context:
{context}

Question:
{query}

Answer:
"""

    answer = generate_response(prompt)

    return {
        "response": answer,
        "sources": sources
    }


if __name__ == "__main__": 
    query = "What are the benefits of travelling?" 
    result = rag_pipeline(query)
    print(result)
    