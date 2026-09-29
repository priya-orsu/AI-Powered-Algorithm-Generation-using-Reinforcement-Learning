import os
import json
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def call_openai_ai(user_prompt: str, algorithm_name: str, category: str) -> dict:
    """Calls OpenAI API to generate comprehensive algorithm JSON from natural language prompt."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key.lower() in ("dummy_key", "your_openai_api_key_here", "none"):
        raise ValueError("No valid OPENAI_API_KEY configured in environment.")

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    configured_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

    openai_client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    prompt = f"""You are an expert Computer Science professor and algorithm architect.

Analyze the user prompt: "{user_prompt}"
Target Algorithm/Task: "{algorithm_name}"
Category: "{category}"

Generate complete, accurate, and highly specific algorithm technical documentation for "{algorithm_name}".

IMPORTANT GUIDELINES:
- "algorithm_name": Clear, standard title for the algorithm (e.g. "{algorithm_name}").
- "category": Appropriate Computer Science domain (e.g. "{category}").
- "description": 2-3 sentences explaining what this algorithm does, how it works, and its core computational strategy.
- "problem_statement": Clear problem description outlining input, objective, and expected output.
- "working_steps": Array of 5-7 clear, sequential step-by-step strings detailing the execution trace of the algorithm on sample input.
- "python_code": Production-ready executable Python code implementation of "{algorithm_name}" with example input data and print statements showing output.
- "pseudocode": Clear, structured algorithm pseudocode incorporating main logic (input/output signatures, variable initializations, core loops, conditionals, return statements).
- "time_complexity": Object with "best", "average", "worst" asymptotic bounds (e.g. "O(1)", "O(N log N)", "O(N^2)").
- "space_complexity": Space complexity bound (e.g. "O(1)", "O(N)", "O(V + E)").
- "resource_usage": Object with "memory" ("Low", "Medium", "High") and "cpu" ("Low", "Medium", "High").
- "advantages": Array of 3 key advantages specific to "{algorithm_name}".
- "disadvantages": Array of 3 key disadvantages or trade-offs specific to "{algorithm_name}".
- "applications": Array of 3 real-world software applications (e.g. Web Indexing, Network Routing, Database Optimization).
- "keywords": Array of 5 relevant search keywords.
- "sample_questions": Array of 3 technical interview questions based on "{algorithm_name}".

Return ONLY valid JSON. Do not include markdown code fences (```json or ```).

JSON Structure:
{{
    "algorithm_name": "{algorithm_name}",
    "category": "{category}",
    "description": "",
    "problem_statement": "",
    "working_steps": [],
    "python_code": "",
    "pseudocode": "",
    "time_complexity": {{
        "best": "",
        "average": "",
        "worst": ""
    }},
    "space_complexity": "",
    "resource_usage": {{
        "memory": "Low",
        "cpu": "Medium"
    }},
    "advantages": [],
    "disadvantages": [],
    "applications": [],
    "keywords": [],
    "sample_questions": []
}}
"""

    models_to_try = [configured_model, "gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    seen = set()
    unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    last_err = None
    for m in unique_models:
        try:
            print(f"[AI Generator] Calling OpenAI model: {m}...")
            response = openai_client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = response.choices[0].message.content
            content = re.sub(r"^```(?:json)?", "", content.strip(), flags=re.IGNORECASE)
            content = re.sub(r"```$", "", content.strip()).strip()
            if "```" in content:
                match = re.search(r"(\{.*\})", content, re.DOTALL)
                if match:
                    content = match.group(1)
            doc = json.loads(content)
            doc["source"] = f"OpenAI ({m})"
            return doc
        except Exception as e:
            last_err = e
            print(f"[AI Generator] OpenAI model {m} failed: {e}. Trying fallback model...")

    raise RuntimeError(f"OpenAI generation failed across models: {last_err}")


def call_openrouter_ai(user_prompt: str, algorithm_name: str, category: str) -> dict:
    """Calls OpenRouter LLM API to synthesize comprehensive algorithm JSON from natural language prompt."""
    prompt = f"""
You are an expert Computer Science professor and algorithm architect.

Analyze the user prompt: "{user_prompt}"
Target Algorithm/Task: "{algorithm_name}"
Category: "{category}"

Generate complete, accurate, and highly specific algorithm technical documentation for "{algorithm_name}".

IMPORTANT GUIDELINES:
- "algorithm_name": Clear, standard title for the algorithm (e.g. "Dijkstra's Shortest Path", "Sieve of Eratosthenes", "QuickSort").
- "category": Appropriate Computer Science domain (Sorting, Graph Algorithms, Dynamic Programming, Searching, String Matching, Mathematics, etc.).
- "description": 2-3 sentences explaining what this algorithm does, how it works, and its core strategy.
- "problem_statement": Clear problem description outlining input, objective, and output.
- "working_steps": Must be a step-by-step array of strings (5-7 steps) detailing the exact step-by-step execution process of "{algorithm_name}" on sample input data.
- "python_code": Production-ready executable Python code implementation of "{algorithm_name}" with example input data and print statements showing output.
- "pseudocode": Clear, structured algorithm pseudocode incorporating main logic (input/output signatures, variable initializations, core loops, conditionals, return statements).
- "time_complexity": Object with "best", "average", "worst" asymptotic bounds (e.g. "O(V + E)", "O(N log N)", "O(N^2)").
- "space_complexity": Space complexity bound (e.g. "O(N)", "O(V)", "O(1)").
- "resource_usage": Memory and CPU usage ratings ("Low", "Medium", "High").
- "advantages": Array of 3 key pros specific to "{algorithm_name}".
- "disadvantages": Array of 3 key cons/limitations specific to "{algorithm_name}".
- "applications": Array of 3 real-world software applications (e.g. GPS Navigation, Network Routing, Compiler Design).
- "keywords": Array of 5 relevant search keywords.
- "sample_questions": Array of 3 candidate interview questions based on "{algorithm_name}".

Return ONLY valid JSON. No markdown codeblocks, no explanations outside JSON.

JSON Structure:
{{
    "algorithm_name": "{algorithm_name}",
    "category": "{category}",
    "description": "",
    "problem_statement": "",
    "working_steps": [],
    "python_code": "",
    "pseudocode": "",
    "time_complexity": {{
        "best": "",
        "average": "",
        "worst": ""
    }},
    "space_complexity": "",
    "resource_usage": {{
        "memory": "Low",
        "cpu": "Medium"
    }},
    "advantages": [],
    "disadvantages": [],
    "applications": [],
    "keywords": [],
    "sample_questions": []
}}
"""
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key or api_key.lower() in ("dummy_key", "none"):
        raise ValueError("No valid OPENROUTER_API_KEY configured in environment.")

    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
    openrouter_client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # Try openrouter models with fallback
    models_to_try = [
        "inclusionai/ling-3.0-flash:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "google/gemini-2.0-flash-lite-preview-02-05:free",
        "openrouter/auto"
    ]

    last_err = None
    for model_name in models_to_try:
        try:
            print(f"[AI Generator] Calling OpenRouter LLM model: {model_name}...")
            response = openrouter_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = response.choices[0].message.content
            content = re.sub(r"```json", "", content, flags=re.IGNORECASE)
            content = re.sub(r"```", "", content).strip()
            doc = json.loads(content)
            doc["source"] = f"OpenRouter AI ({model_name})"
            return doc
        except Exception as e:
            last_err = e
            print(f"[AI Generator] Model {model_name} failed: {e}. Trying next fallback model...")

    raise RuntimeError(f"OpenRouter LLM generation failed across models: {last_err}")


def generate_algorithm_document(algorithm_name: str, category: str = "General"):
    """
    Generates and optimizes an algorithm document using:
    1. OpenAI LLM (if OPENAI_API_KEY is configured)
    2. OpenRouter LLM (if OPENROUTER_API_KEY is configured)
    3. Local Hybrid GA-RL Metaheuristic Engine (always available, 100% reliable fallback)
    """
    from app.services.prompt_parser import parse_user_prompt

    parsed_info = parse_user_prompt(algorithm_name)
    if not parsed_info["is_valid"]:
        raise ValueError(parsed_info.get("reason", "Invalid prompt or algorithm query."))

    target_name = parsed_info.get("matched_algorithm", algorithm_name)
    target_category = parsed_info.get("category", category)

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"

    # Priority 1: OpenAI API
    if openai_key and openai_key.lower() not in ("dummy_key", "your_openai_api_key_here", "none"):
        try:
            print(f"\n[AI Generator] Attempting algorithm generation for '{target_name}' via OpenAI API...")
            doc = call_openai_ai(
                user_prompt=algorithm_name,
                algorithm_name=target_name,
                category=target_category
            )
            print(f"[AI Generator] Successfully generated '{target_name}' via {doc.get('source')}!")
            return doc
        except Exception as openai_err:
            print(f"[AI Generator] OpenAI generation failed ({openai_err}). Checking next fallback...")

    # Priority 2: OpenRouter API
    if (use_openrouter or openrouter_key) and openrouter_key and openrouter_key.lower() not in ("dummy_key", "none"):
        try:
            print(f"\n[AI Generator] Attempting algorithm generation for '{target_name}' via OpenRouter API...")
            doc = call_openrouter_ai(
                user_prompt=algorithm_name,
                algorithm_name=target_name,
                category=target_category
            )
            print(f"[AI Generator] Successfully generated '{target_name}' via {doc.get('source')}!")
            return doc
        except Exception as ai_err:
            print(f"[AI Generator] OpenRouter generation failed ({ai_err}). Falling back to Hybrid GA-RL Engine...")

    # Priority 3: Primary Hybrid GA-RL Engine Fallback (Simulated Annealing + PSO + GA + RL)
    try:
        print(f"\n[AI Generator] Generating '{target_name}' via Hybrid GA-RL Metaheuristic Engine...")
        from app.services.hybrid_garl import hybrid_garl_engine
        result = hybrid_garl_engine.generate_and_optimize(
            algorithm_name=target_name,
            category=target_category,
            user_prompt=algorithm_name,
            parsed_prompt_info=parsed_info
        )
        document = result["document"]
        document["source"] = "Hybrid GA-RL Engine"
        print(f"[AI Generator] Successfully generated '{target_name}' via Hybrid GA-RL Engine!")
        return document

    except Exception as garl_err:
        print(f"\n[AI Generator] Primary Hybrid GA-RL Engine failed ({garl_err}).")
        raise RuntimeError(f"Failed to generate algorithm documentation for '{algorithm_name}': {garl_err}")


def verify_algorithm_with_openai(prompt: str) -> dict:
    """Checks with OpenAI if the prompt is an established, recognized computer science algorithm."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key.lower() in ("dummy_key", "your_openai_api_key_here", "none"):
        return {"is_defined": False}

    try:
        openai_client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
        )
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
        verify_prompt = f"""You are a strict Computer Science algorithm validator.
Determine if the following query refers to an established, recognized Computer Science algorithm, data structure, or well-defined CS algorithmic problem:
Query: "{prompt}"

CRITICAL RULES:
- If the query is an everyday word, physical object, animal, food, personal name, college/school name, company, greeting, or non-algorithmic topic (e.g. "car", "apple", "banana", "Habeeb", "Vignan Lara", "football", "hello", "laptop"), return {{"is_defined": false}}.
- If and ONLY if the query refers to an established, recognized Computer Science algorithm or data structure (e.g. "Dijkstra", "QuickSort", "PageRank", "A* Search", "Bloom Filter", "Convex Hull", "Chandy-Lamport", "K-Means", "RSA"), return {{"is_defined": true, "standard_name": "<Standard Title>", "category": "<CS Domain>"}}.

Return ONLY valid JSON.
"""
        response = openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": verify_prompt}],
            temperature=0.0
        )
        content = response.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?", "", content, flags=re.IGNORECASE)
        content = re.sub(r"```$", "", content).strip()
        doc = json.loads(content)
        return doc
    except Exception as e:
        print(f"[AI Validator] OpenAI validation check failed: {e}")
        return {"is_defined": False}