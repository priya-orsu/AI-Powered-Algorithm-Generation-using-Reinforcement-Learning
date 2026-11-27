import re


def parse_ai_response(name, response):

    def extract(title):

        patterns = [

            rf"##\s*\*\*{title}\*\*(.*?)(?=\n##|\Z)",

            rf"##\s*{title}(.*?)(?=\n##|\Z)",

            rf"###\s*\*\*{title}\*\*(.*?)(?=\n###|\n##|\Z)",

            rf"###\s*{title}(.*?)(?=\n###|\n##|\Z)"

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                response,
                re.IGNORECASE | re.DOTALL
            )

            if match:
                return match.group(1).strip()

        return ""

    return {

        "algorithm_name": name,

        "category": "AI Generated",

        "description": extract("Description"),

        "working_steps": extract("Working Steps"),

        "time_complexity": extract("Time Complexity"),

        "space_complexity": extract("Space Complexity"),

        "applications": extract("Applications"),

        "advantages": extract("Advantages"),

        "disadvantages": extract("Disadvantages"),

        "python_code": extract("Python Implementation"),

        "keywords": [name.lower()],

        "source": "OpenRouter AI"

    }