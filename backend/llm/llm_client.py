import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # best free + fast
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

if __name__=="__main__":
    print(generate_response("what is ai"))
