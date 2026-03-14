from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_documentation(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior software engineer. "
                    "Generate professional documentation based ONLY on the given analysis."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2500
    )

    print("RAW LLM RESPONSE ↓↓↓")
    print(response)
    print("RAW LLM RESPONSE ↑↑↑")

    if not response.choices:
        return "LLM returned no choices."

    if not response.choices[0].message:
        return "LLM returned no message."

    if not response.choices[0].message.content:
        return "LLM returned empty content."

    return response.choices[0].message.content
