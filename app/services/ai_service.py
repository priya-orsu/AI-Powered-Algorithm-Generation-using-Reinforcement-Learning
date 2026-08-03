from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1")
)

def ask_ai(question: str):

    try:
        response = client.chat.completions.create(
            model="openrouter-small-latest",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Computer Science professor. "
                        "Explain algorithms with description, working steps, "
                        "time complexity, space complexity, applications, "
                        "advantages, disadvantages, and Python implementation."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {e}"