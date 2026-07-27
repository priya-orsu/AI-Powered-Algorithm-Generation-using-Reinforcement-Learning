from fastapi import APIRouter
from datetime import datetime
import time

from app.database.connection import (
    algorithm_collection,
    query_history_collection,
    generation_log_collection,
    performance_metrics_collection
)

from app.services.ai_generator import generate_algorithm_document

router = APIRouter()


# ============================================================
# SEARCH ALGORITHM
# ============================================================

@router.get("/algorithm/{algorithm_name}")
def get_algorithm_by_name(algorithm_name: str):

    start_time = time.time()

    # Search MongoDB
    algorithm = algorithm_collection.find_one(
        {
            "algorithm_name": {
                "$regex": f"^{algorithm_name}$",
                "$options": "i"
            }
        },
        {
            "_id": 0
        }
    )

    print("\n========== MONGODB SEARCH ==========")
    print("Searching :", algorithm_name)
    print("Found :", algorithm)
    print("====================================\n")

    response_time = round((time.time() - start_time) * 1000, 2)

    # =======================================================
    # FOUND IN DATABASE
    # =======================================================

    if algorithm:

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

            {

                "algorithm_name": algorithm_name

            },

            {

                "$inc": {

                    "search_count": 1

                },

                "$set": {

                    "last_accessed": datetime.now(),

                    "average_response_time_ms": response_time

                }

            },

            upsert=True

        )

        return {

            "status": "success",

            "source": "MongoDB",

            "response_time_ms": response_time,

            "data": algorithm

        }

    # =======================================================
    # NOT FOUND → GENERATE USING AI
    # =======================================================

    try:

        algorithm_document = generate_algorithm_document(
            algorithm_name
        )

        print("\n========== AI GENERATED ==========")
        print("User searched :", algorithm_name)
        print("Stored as     :", algorithm_document.get("algorithm_name"))
        print("=================================\n")

        algorithm_collection.insert_one(
            algorithm_document
        )

        # Remove ObjectId before returning response
        algorithm_document.pop("_id", None)

        query_history_collection.insert_one({

            "query": algorithm_name,

            "search_type": "Algorithm",

            "status": "AI Generated",

            "timestamp": datetime.now()

        })

        generation_log_collection.insert_one({

            "algorithm_name": algorithm_name,

            "status": "generated",

            "source": "OpenRouter AI",

            "timestamp": datetime.now()

        })

        performance_metrics_collection.update_one(

            {

                "algorithm_name": algorithm_name

            },

            {

                "$inc": {

                    "search_count": 1

                },

                "$set": {

                    "last_accessed": datetime.now(),

                    "average_response_time_ms": response_time

                }

            },

            upsert=True

        )

        return {

            "status": "success",

            "source": "OpenRouter AI",

            "response_time_ms": response_time,

            "message": "Algorithm generated successfully.",

            "data": algorithm_document

        }

    except Exception as e:

        generation_log_collection.insert_one({

            "algorithm_name": algorithm_name,

            "status": "failed",

            "source": "OpenRouter AI",

            "error": str(e),

            "timestamp": datetime.now()

        })

        return {

            "status": "error",

            "message": str(e)

        }


# ============================================================
# CATEGORY SEARCH
# ============================================================

@router.get("/category/{category_name}")
def get_algorithms_by_category(category_name: str):

    algorithms = list(

        algorithm_collection.find(

            {

                "category": {

                    "$regex": category_name,

                    "$options": "i"

                }

            },

            {

                "_id": 0

            }

        )

    )

    query_history_collection.insert_one({

        "query": category_name,

        "search_type": "Category",

        "status": "Found" if algorithms else "Not Found",

        "timestamp": datetime.now()

    })

    if algorithms:

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
# KEYWORD SEARCH
# ============================================================

@router.get("/keyword/{keyword}")
def get_algorithms_by_keyword(keyword: str):

    algorithms = list(

        algorithm_collection.find(

            {

                "keywords": {

                    "$regex": keyword,

                    "$options": "i"

                }

            },

            {

                "_id": 0

            }

        )

    )

    query_history_collection.insert_one({

        "query": keyword,

        "search_type": "Keyword",

        "status": "Found" if algorithms else "Not Found",

        "timestamp": datetime.now()

    })

    if algorithms:

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
# APPLICATION SEARCH
# ============================================================

@router.get("/application/{application}")
def get_algorithms_by_application(application: str):

    algorithms = list(

        algorithm_collection.find(

            {
                "applications": {
                    "$regex": application,
                    "$options": "i"
                }
            },

            {
                "_id": 0
            }

        )

    )

    query_history_collection.insert_one({

        "query": application,

        "search_type": "Application",

        "status": "Found" if algorithms else "Not Found",

        "timestamp": datetime.now()

    })

    if algorithms:

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

        performance_metrics_collection.find(

            {},

            {

                "_id": 0

            }

        )

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

    found_queries = query_history_collection.count_documents({

        "status": "Found"

    })

    ai_generated_queries = query_history_collection.count_documents({

        "status": "AI Generated"

    })

    total_generations = generation_log_collection.count_documents({})

    retrieved = generation_log_collection.count_documents({

        "status": "retrieved"

    })

    generated = generation_log_collection.count_documents({

        "status": "generated"

    })

    failed = generation_log_collection.count_documents({

        "status": "failed"

    })

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

        performance_metrics_collection.find(

            {},

            {

                "_id": 0

            }

        ).sort(

            "search_count",

            -1

        ).limit(10)

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

        algorithm_collection.find(

            {},

            {

                "_id": 0

            }

        )

    )

    return {

        "status": "success",

        "count": len(algorithms),

        "data": algorithms

    }