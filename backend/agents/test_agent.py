from backend.llm.llm_client import generate_response

def test_agent(query: str):

    prompt = f"""
You are a software testing expert.

Generate 3–5 test cases for the following requirement:

{query}

Instructions:
- Be clear and practical
- Keep steps simple

Format:

Test Case 1:
Description:
Steps:
Expected Result:

Test Case 2:
Description:
Steps:
Expected Result:

Test Case 3:
Description:
Steps:
Expected Result:
"""

    return generate_response(prompt)