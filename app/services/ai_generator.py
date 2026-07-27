import os
import json
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def generate_algorithm_document(algorithm_name: str):

    prompt = f"""
You are an expert Computer Science professor.

Generate complete information about the algorithm "{algorithm_name}".

Return ONLY valid JSON.

The JSON must exactly match this structure:

{{
    "algorithm_name": "",
    "category": "",
    "description": "",
    "problem_statement": "",
    "working_steps": [
        "",
        "",
        ""
    ],
    "time_complexity": {{
        "best": "",
        "average": "",
        "worst": ""
    }},
    "space_complexity": "",
    "resource_usage": {{
        "memory": "",
        "cpu": ""
    }},
    "advantages": [],
    "disadvantages": [],
    "applications": [],
    "keywords": [],
    "sample_questions": []
}}

Do not include markdown.
Do not include explanations.
Return ONLY the JSON object.
"""

    response = client.chat.completions.create(

        # Free model (change if OpenRouter rotates free models)
        model="inclusionai/ling-3.0-flash:free",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    content = response.choices[0].message.content

    print("\n========== AI RESPONSE ==========")
    print(content)
    print("=================================\n")

    # Remove Markdown code fences if present
    content = re.sub(r"```json", "", content, flags=re.IGNORECASE)
    content = re.sub(r"```", "", content)
    content = content.strip()

    try:
        return json.loads(content)

    except Exception as e:

        print("JSON Parsing Error:", e)

        return {
            "algorithm_name": algorithm_name,
            "category": "AI Generated",
            "description": content,
            "problem_statement": "",
            "working_steps": [],
            "time_complexity": {
                "best": "",
                "average": "",
                "worst": ""
            },
            "space_complexity": "",
            "resource_usage": {
                "memory": "",
                "cpu": ""
            },
            "advantages": [],
            "disadvantages": [],
            "applications": [],
            "keywords": [algorithm_name],
            "sample_questions": []
        }