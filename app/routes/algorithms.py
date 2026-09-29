import os
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import time
import re

from app.database.connection import (
    algorithm_collection,
    query_history_collection,
    generation_log_collection,
    performance_metrics_collection
)

from app.services.ai_generator import generate_algorithm_document
from app.services.prompt_parser import parse_user_prompt
from app.services.problem_solver import solve_problem_pipeline, simulate_dynamic_training, simulate_test_evaluation
from app.services.leetcode_catalog import get_leetcode_problems_for_algorithm

router = APIRouter()


from typing import Optional

class ProblemRunCodeRequest(BaseModel):
    code: str
    timeout_sec: Optional[int] = 10


class ProblemTrainRequest(BaseModel):
    algorithm: Optional[str] = "Hybrid GA-RL Routing Optimizer"
    episodes: Optional[int] = 1000
    learning_rate: Optional[float] = 0.001
    epsilon: Optional[float] = 0.05
    batch_size: Optional[int] = 64
    primary_metric_name: Optional[str] = None
    primary_metric_value: Optional[float] = None
    primary_metric_unit: Optional[str] = None
    secondary_metric_name: Optional[str] = None
    secondary_metric_value: Optional[float] = None
    secondary_metric_unit: Optional[str] = None


class ProblemEvaluateRequest(BaseModel):
    algorithm: Optional[str] = "Hybrid GA-RL Routing Optimizer"
    test_episodes: Optional[int] = 100
    primary_metric_name: Optional[str] = None
    primary_metric_value: Optional[float] = None
    primary_metric_unit: Optional[str] = None
    secondary_metric_name: Optional[str] = None
    secondary_metric_value: Optional[float] = None
    secondary_metric_unit: Optional[str] = None


class InterviewAskRequest(BaseModel):
    question: str


class ProblemRequest(BaseModel):
    problem: Optional[str] = None
    problem_description: Optional[str] = None



# ============================================================

def enrich_algorithm_with_leetcode(algo_dict: dict) -> dict:
    if not isinstance(algo_dict, dict):
        return algo_dict
    name = algo_dict.get("algorithm_name", "")
    cat = algo_dict.get("category", "")
    kw = algo_dict.get("keywords", [])
    desc = algo_dict.get("description", "")
    from app.services.algorithm_definition_catalog import get_authentic_algorithm_definition
    if not desc or "Generated using Tri-Hybrid" in desc or "Locates target elements" in desc:
        desc = get_authentic_algorithm_definition(name, cat)
        algo_dict["description"] = desc
        if "_id" in algo_dict:
            try:
                algorithm_collection.update_one({"_id": algo_dict["_id"]}, {"$set": {"description": desc}})
            except Exception:
                pass

    # 1. Attach suitable LeetCode problems
    problems = get_leetcode_problems_for_algorithm(
        algorithm_name=name,
        category=cat,
        keywords=kw,
        description=desc
    )
    algo_dict["leetcode_problems"] = problems
    algo_dict["primary_leetcode_problem"] = problems[0] if problems else None

    # 2. Attach human-understandable, efficient overview breakdown
    try:
        from app.services.algorithm_overview_service import generate_algorithm_overview
        overview_info = generate_algorithm_overview(
            algorithm_name=name,
            category=cat,
            description=desc,
            problem_statement=stmt
        )
        algo_dict["overview_meta"] = overview_info
    except Exception as e:
        print("[Overview Enrichment Warning]", e)

    # 3. Attach comprehensive technical interview Q&A with model answers
    try:
        from app.services.algorithm_interview_service import get_algorithm_interview_qa
        qas = get_algorithm_interview_qa(
            algorithm_name=name,
            category=cat,
            problem_statement=stmt,
            time_complexity=str(algo_dict.get("time_complexity", "O(N log N)")),
            space_complexity=str(algo_dict.get("space_complexity", "O(N)"))
        )
        algo_dict["interview_qa"] = qas
        if not algo_dict.get("sample_questions"):
            algo_dict["sample_questions"] = [item["question"] for item in qas]
    except Exception as e:
        print("[Interview Q&A Enrichment Warning]", e)

    return algo_dict

# ============================================================
# SEARCH ALGORITHM BY NAME (WITH GA+RL FALLBACK & PROMPT PARSER)
# ============================================================

@router.post("/algorithm/{algorithm_name:path}/ask-interview")
def ask_algorithm_interview(algorithm_name: str, req: InterviewAskRequest):
    from app.services.algorithm_interview_service import answer_custom_interview_question
    ans = answer_custom_interview_question(
        algorithm_name=algorithm_name,
        question=req.question
    )
    return {
        "status": "success",
        "data": ans
    }


@router.get("/algorithm/{algorithm_name:path}/leetcode")
def get_algorithm_leetcode(algorithm_name: str):
    parsed_info = parse_user_prompt(algorithm_name)
    target_name = parsed_info.get("matched_algorithm", algorithm_name)
    category_hint = parsed_info.get("category")
    
    # Try fetching from DB to get keywords/description
    algo = algorithm_collection.find_one({"algorithm_name": {"$regex": f"^{re.escape(target_name)}$", "$options": "i"}}, {"_id": 0})
    if algo:
        problems = get_leetcode_problems_for_algorithm(
            algorithm_name=algo.get("algorithm_name", target_name),
            category=algo.get("category", category_hint),
            keywords=algo.get("keywords", []),
            description=algo.get("description", "")
        )
    else:
        problems = get_leetcode_problems_for_algorithm(
            algorithm_name=target_name,
            category=category_hint
        )

    return {
        "status": "success",
        "algorithm_name": target_name,
        "count": len(problems),
        "primary_problem": problems[0] if problems else None,
        "data": problems
    }


@router.get("/algorithm/{algorithm_name:path}")
def get_algorithm_by_name(algorithm_name: str):
    start_time = time.time()

    # Step 1: Validate and parse user input prompt
    parsed_info = parse_user_prompt(algorithm_name)
    if not parsed_info["is_valid"]:
        return {
            "status": "invalid_prompt",
            "message": parsed_info.get("reason", "Invalid prompt: Could not understand user query.")
        }

    clean_query = algorithm_name.strip()
    target_name = parsed_info.get("matched_algorithm", clean_query)

    # Build candidate keys for comprehensive database matching
    candidate_names = [target_name, clean_query]
    
    # Variations without 'Algorithm' suffix
    if target_name.lower().endswith(" algorithm"):
        candidate_names.append(target_name[:-10].strip())
    else:
        candidate_names.append(f"{target_name} Algorithm")
    if clean_query.lower().endswith(" algorithm"):
        candidate_names.append(clean_query[:-10].strip())
    else:
        candidate_names.append(f"{clean_query} Algorithm")

    # Variations without parentheses acronyms (e.g. 'Simple Genetic Algorithm (SGA)' -> 'Simple Genetic Algorithm')
    no_paren_target = re.sub(r"\s*\([^)]*\)", "", target_name).strip()
    if no_paren_target and no_paren_target != target_name:
        candidate_names.append(no_paren_target)
        if not no_paren_target.lower().endswith(" algorithm"):
            candidate_names.append(f"{no_paren_target} Algorithm")

    seen_names = set()
    unique_candidates = [n for n in candidate_names if n and not (n.lower() in seen_names or seen_names.add(n.lower()))]

    # Step 2: Check MongoDB first
    or_clauses = [{"algorithm_name": {"$regex": f"^{re.escape(name)}$", "$options": "i"}} for name in unique_candidates]
    or_clauses.append({"keywords": {"$regex": f"^{re.escape(clean_query)}$", "$options": "i"}})
    or_clauses.append({"keywords": {"$regex": f"^{re.escape(target_name)}$", "$options": "i"}})

    algorithm = algorithm_collection.find_one(
        {"$or": or_clauses},
        {"_id": 0}
    )

    print("\n========== MONGODB SEARCH ==========")
    print("Searching :", algorithm_name)
    print("Found in DB :", algorithm.get("algorithm_name") if algorithm else "None (Will generate dynamically)")
    print("====================================\n")

    response_time = round((time.time() - start_time) * 1000, 2)

    # Check if retrieved document is a placeholder that requires re-synthesis
    is_placeholder = False
    if algorithm:
        py_code = algorithm.get("python_code", "")
        if "processed = sorted(data)" in py_code and "sort" not in target_name.lower():
            is_placeholder = True

    # 1. RETRIEVED DIRECTLY FROM MONGODB DATABASE
    if algorithm and not is_placeholder:
        query_history_collection.insert_one({
            "query": algorithm_name,
            "search_type": "Algorithm",
            "status": "Found",
            "timestamp": datetime.now()
        })

        generation_log_collection.insert_one({
            "algorithm_name": algorithm_name,
            "status": "retrieved",
            "source": "MongoDB",
            "timestamp": datetime.now()
        })

        performance_metrics_collection.update_one(
            {"algorithm_name": algorithm.get("algorithm_name", target_name)},
            {
                "$inc": {"search_count": 1},
                "$set": {
                    "last_accessed": datetime.now(),
                    "average_response_time_ms": response_time
                }
            },
            upsert=True
        )

        enrich_algorithm_with_leetcode(algorithm)
        return {
            "status": "success",
            "source": "MongoDB",
            "response_time_ms": response_time,
            "message": f"Algorithm '{algorithm.get('algorithm_name')}' retrieved directly from MongoDB database.",
            "data": algorithm
        }

    # 2. NOT IN DB → DYNAMICALLY GENERATE (OPENAI -> OPENROUTER -> HYBRID GA-RL ENGINE)
    try:
        category_hint = parsed_info.get("category", "General")
        algorithm_document = generate_algorithm_document(algorithm_name=algorithm_name, category=category_hint)
        source_name = algorithm_document.get("source", "Hybrid GA-RL Engine")
        stored_name = algorithm_document.get("algorithm_name", target_name)

        print("\n========== ALGORITHM GENERATED ==========")
        print("User searched :", algorithm_name)
        print("Synthesized as:", stored_name)
        print("Engine Source :", source_name)
        print("Persisting to MongoDB...")
        print("=========================================\n")

        # Ensure authentic, clean definition before saving
        from app.services.algorithm_definition_catalog import get_authentic_algorithm_definition
        curr_desc = algorithm_document.get("description", "")
        if not curr_desc or "Generated using Tri-Hybrid" in curr_desc or "Locates target elements" in curr_desc:
            algorithm_document["description"] = get_authentic_algorithm_definition(stored_name, category_hint, algorithm_name)

        # Automatically persist newly generated algorithm to MongoDB
        algorithm_collection.update_one(
            {"algorithm_name": {"$regex": f"^{re.escape(stored_name)}$", "$options": "i"}},
            {"$set": algorithm_document},
            upsert=True
        )
        algorithm_document.pop("_id", None)

        query_history_collection.insert_one({
            "query": algorithm_name,
            "search_type": "Algorithm",
            "status": "Generated",
            "timestamp": datetime.now()
        })

        generation_log_collection.insert_one({
            "algorithm_name": stored_name,
            "status": "generated",
            "source": source_name,
            "timestamp": datetime.now()
        })

        performance_metrics_collection.update_one(
            {"algorithm_name": stored_name},
            {
                "$inc": {"search_count": 1},
                "$set": {
                    "last_accessed": datetime.now(),
                    "average_response_time_ms": response_time
                }
            },
            upsert=True
        )

        enrich_algorithm_with_leetcode(algorithm_document)
        return {
            "status": "success",
            "source": source_name,
            "response_time_ms": response_time,
            "message": f"Algorithm '{stored_name}' generated via {source_name} and saved to MongoDB.",
            "data": algorithm_document
        }

    except Exception as e:
        generation_log_collection.insert_one({
            "algorithm_name": algorithm_name,
            "status": "failed",
            "source": "Generation Engine",
            "error": str(e),
            "timestamp": datetime.now()
        })

        return {
            "status": "error",
            "message": f"Failed to generate algorithm: {str(e)}"
        }


# ============================================================
# CATEGORY SEARCH (MULTI-FIELD MATCHING)
# ============================================================

@router.get("/category/{category_name}")
def get_algorithms_by_category(category_name: str):
    regex_pattern = {"$regex": category_name, "$options": "i"}

    algorithms = list(
        algorithm_collection.find(
            {
                "$or": [
                    {"category": regex_pattern},
                    {"algorithm_name": regex_pattern},
                    {"description": regex_pattern}
                ]
            },
            {"_id": 0}
        )
    )

    query_history_collection.insert_one({
        "query": category_name,
        "search_type": "Category",
        "status": "Found" if algorithms else "Not Found",
        "timestamp": datetime.now()
    })

    if algorithms:
        for a in algorithms:
            enrich_algorithm_with_leetcode(a)
        return {
            "status": "success",
            "count": len(algorithms),
            "data": algorithms
        }

    return {
        "status": "not_found",
        "message": "No algorithms found."
    }


# ============================================================
# KEYWORD SEARCH (MULTI-FIELD MATCHING)
# ============================================================

@router.get("/keyword/{keyword}")
def get_algorithms_by_keyword(keyword: str):
    regex_pattern = {"$regex": keyword, "$options": "i"}

    algorithms = list(
        algorithm_collection.find(
            {
                "$or": [
                    {"keywords": regex_pattern},
                    {"algorithm_name": regex_pattern},
                    {"category": regex_pattern},
                    {"description": regex_pattern},
                    {"problem_statement": regex_pattern}
                ]
            },
            {"_id": 0}
        )
    )

    query_history_collection.insert_one({
        "query": keyword,
        "search_type": "Keyword",
        "status": "Found" if algorithms else "Not Found",
        "timestamp": datetime.now()
    })

    if algorithms:
        for a in algorithms:
            enrich_algorithm_with_leetcode(a)
        return {
            "status": "success",
            "count": len(algorithms),
            "data": algorithms
        }

    return {
        "status": "not_found",
        "message": "No matching algorithms."
    }


# ============================================================
# APPLICATION SEARCH (MULTI-FIELD MATCHING)
# ============================================================

@router.get("/application/{application}")
def get_algorithms_by_application(application: str):
    regex_pattern = {"$regex": application, "$options": "i"}

    algorithms = list(
        algorithm_collection.find(
            {
                "$or": [
                    {"applications": regex_pattern},
                    {"algorithm_name": regex_pattern},
                    {"description": regex_pattern},
                    {"problem_statement": regex_pattern},
                    {"category": regex_pattern}
                ]
            },
            {"_id": 0}
        )
    )

    query_history_collection.insert_one({
        "query": application,
        "search_type": "Application",
        "status": "Found" if algorithms else "Not Found",
        "timestamp": datetime.now()
    })

    if algorithms:
        for a in algorithms:
            enrich_algorithm_with_leetcode(a)
        return {
            "status": "success",
            "count": len(algorithms),
            "data": algorithms
        }

    return {
        "status": "not_found",
        "message": "No matching applications."
    }


# ============================================================
# PERFORMANCE METRICS
# ============================================================

@router.get("/performance")
def get_performance_metrics():
    metrics = list(
        performance_metrics_collection.find({}, {"_id": 0})
    )
    return {
        "status": "success",
        "count": len(metrics),
        "data": metrics
    }


# ============================================================
# BACKEND STATISTICS
# ============================================================

@router.get("/statistics")
def get_statistics():
    total_algorithms = algorithm_collection.count_documents({})
    total_queries = query_history_collection.count_documents({})
    found_queries = query_history_collection.count_documents({"status": "Found"})
    ai_generated_queries = query_history_collection.count_documents({
        "status": {"$in": ["AI Generated", "GA+RL Generated", "garl_optimized"]}
    })
    total_generations = generation_log_collection.count_documents({})
    retrieved = generation_log_collection.count_documents({"status": "retrieved"})
    generated = generation_log_collection.count_documents({"status": "generated"})
    failed = generation_log_collection.count_documents({"status": "failed"})
    total_performance_records = performance_metrics_collection.count_documents({})

    return {
        "status": "success",
        "statistics": {
            "total_algorithms": total_algorithms,
            "total_queries": total_queries,
            "found_queries": found_queries,
            "ai_generated_queries": ai_generated_queries,
            "total_generations": total_generations,
            "generated": generated,
            "retrieved": retrieved,
            "failed": failed,
            "performance_records": total_performance_records
        }
    }


# ============================================================
# TOP SEARCHED ALGORITHMS
# ============================================================

@router.get("/performance/top")
def get_top_algorithms():
    algorithms = list(
        performance_metrics_collection.find({}, {"_id": 0}).sort("search_count", -1).limit(5)
    )
    return {
        "status": "success",
        "count": len(algorithms),
        "data": algorithms
    }


# ============================================================
# GET ALL ALGORITHMS
# ============================================================

@router.get("/algorithms")
def get_all_algorithms():
    algorithms = list(
        algorithm_collection.find({}, {"_id": 0})
    )
    return {
        "status": "success",
        "count": len(algorithms),
        "data": algorithms
    }


# ============================================================
# PROBLEM-TO-ALGORITHM WORKFLOW PIPELINE (10-STAGE SOLVER)
# ============================================================

@router.post("/problem/solve")
def solve_problem_endpoint(req: ProblemRequest):
    start_time = time.time()
    problem_text = (req.problem or req.problem_description or "").strip()
    if not problem_text:
        problem_text = "Formulate and solve general multi-objective computational optimization problem"
    result = solve_problem_pipeline(problem_text)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    query_history_collection.insert_one({
        "query": problem_text,
        "search_type": "Problem",
        "status": "Solved",
        "timestamp": datetime.now(),
        "best_algorithm": result.get("best_algorithm", {}).get("algorithm_name") or result.get("best_algorithm", {}).get("name"),
        "problem_type": result.get("classification", {}).get("primary_class")
    })

    return {
        "status": "success",
        "duration_ms": duration_ms,
        "data": result
    }


@router.get("/problem/{problem_text:path}")
def solve_problem_get_endpoint(problem_text: str):
    start_time = time.time()
    result = solve_problem_pipeline(problem_text)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    query_history_collection.insert_one({
        "query": problem_text,
        "search_type": "Problem",
        "status": "Solved",
        "timestamp": datetime.now(),
        "best_algorithm": result.get("best_algorithm", {}).get("name"),
        "problem_type": result.get("classification", {}).get("primary_class")
    })

    return {
        "status": "success",
        "duration_ms": duration_ms,
        "data": result
    }


@router.post("/problem/train")
def train_problem_endpoint(req: ProblemTrainRequest):
    algo = req.algorithm or "Hybrid GA-RL Routing Optimizer"
    eps = req.episodes or 1000
    lr = req.learning_rate or 0.001
    epsilon = req.epsilon if req.epsilon is not None else 0.05
    bs = req.batch_size or 64
    res = simulate_dynamic_training(
        algorithm=algo,
        episodes=eps,
        learning_rate=lr,
        epsilon=epsilon,
        batch_size=bs,
        primary_metric_name=req.primary_metric_name,
        primary_metric_value=req.primary_metric_value,
        primary_metric_unit=req.primary_metric_unit,
        secondary_metric_name=req.secondary_metric_name,
        secondary_metric_value=req.secondary_metric_value,
        secondary_metric_unit=req.secondary_metric_unit
    )
    return res


@router.post("/problem/evaluate")
def evaluate_problem_endpoint(req: ProblemEvaluateRequest):
    algo = req.algorithm or "Hybrid GA-RL Routing Optimizer"
    test_eps = req.test_episodes or 100
    res = simulate_test_evaluation(
        algorithm=algo,
        test_episodes=test_eps,
        primary_metric_name=req.primary_metric_name,
        primary_metric_value=req.primary_metric_value,
        primary_metric_unit=req.primary_metric_unit,
        secondary_metric_name=req.secondary_metric_name,
        secondary_metric_value=req.secondary_metric_value,
        secondary_metric_unit=req.secondary_metric_unit
    )
    return res


@router.post("/problem/run-code")
def run_code_endpoint(req: ProblemRunCodeRequest):
    import subprocess, sys, time, tempfile, os
    start = time.time()
    code_text = (req.code or "").strip()
    if not code_text:
        return {
            "status": "error",
            "exit_code": 1,
            "stdout": "",
            "stderr": "No code provided to execute",
            "duration_ms": 0.0
        }
    
    temp_path = None
    timeout = min(req.timeout_sec or 10, 15)
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(code_text)
            temp_path = f.name
        
        proc = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "status": "success",
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration_ms": duration_ms
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution timed out (limit: {timeout} seconds)",
            "duration_ms": round((time.time() - start) * 1000, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "exit_code": 1,
            "stdout": "",
            "stderr": str(e),
            "duration_ms": round((time.time() - start) * 1000, 2)
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


from fastapi.responses import FileResponse
from fastapi import HTTPException

@router.get("/download/presentation")
@router.get("/presentation/download")
def download_presentation_file():
    target = r"C:\Users\HP 840 G6\Desktop\AI-Powered-Algorithm-Generation-using-Reinforcement-Learning-main (2)\AlgoGen_Studio_Presentation.pptx"
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="Presentation file not found")
    return FileResponse(
        target,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="AlgoGen_Studio_Presentation.pptx"
    )