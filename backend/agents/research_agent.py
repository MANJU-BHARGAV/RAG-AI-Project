from backend.llm.llm_client import generate_response

def research_agent(query: str):

    prompt = f"""
You are a research assistant.

Write a clear and structured report on the topic below.

Topic: {query}

Instructions:
- Use simple and clear language
- Keep it concise (5–8 sentences)
- Organize into sections

Format:
Introduction:
Key Points:
Applications:
Conclusion:

Report:
"""

    return generate_response(prompt)