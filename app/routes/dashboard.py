from fastapi import APIRouter

from app.database.connection import (
    algorithm_collection,
    query_history_collection,
    generation_log_collection,
    performance_metrics_collection,
    api_log_collection
)

router = APIRouter()


# ============================================================
# DASHBOARD ANALYTICS
# ============================================================

@router.get("/dashboard")
def get_dashboard():

    # Total Algorithms
    total_algorithms = algorithm_collection.count_documents({})

    # Total Searches
    total_queries = query_history_collection.count_documents({})

    # Retrieved from MongoDB
    retrieved_algorithms = generation_log_collection.count_documents({
        "status": "retrieved"
    })

    # Generated using AI
    generated_algorithms = generation_log_collection.count_documents({
        "status": "generated"
    })

    # Failed Generations
    failed_generations = generation_log_collection.count_documents({
        "status": "failed"
    })

    # ----------------------------------------
    # Most Searched Algorithm
    # ----------------------------------------

    top_algorithm = performance_metrics_collection.find_one(
        sort=[("search_count", -1)]
    )

    if top_algorithm:
        most_searched_algorithm = top_algorithm["algorithm_name"]
    else:
        most_searched_algorithm = "N/A"

    # ----------------------------------------
    # Latest Search
    # ----------------------------------------

    latest_query = query_history_collection.find_one(
        sort=[("timestamp", -1)]
    )

    if latest_query:
        latest_search = latest_query["query"]
    else:
        latest_search = "N/A"

    # ----------------------------------------
    # Average Response Time
    # ----------------------------------------

    metrics = list(
        performance_metrics_collection.find(
            {},
            {
                "_id": 0,
                "average_response_time_ms": 1
            }
        )
    )

    if metrics:

        total = sum(
            item["average_response_time_ms"]
            for item in metrics
        )

        average_response = round(
            total / len(metrics),
            2
        )

    else:

        average_response = 0

    # ----------------------------------------

    return {

        "status": "success",

        "dashboard": {

            "total_algorithms": total_algorithms,

            "total_queries": total_queries,

            "retrieved_algorithms": retrieved_algorithms,

            "generated_algorithms": generated_algorithms,

            "failed_generations": failed_generations,

            "most_searched_algorithm": most_searched_algorithm,

            "latest_search": latest_search,

            "average_response_time_ms": average_response

        }

    }
# ============================================================
# TOP SEARCHED ALGORITHMS
# ============================================================

@router.get("/dashboard/top-algorithms")
def top_algorithms():

    algorithms = list(

        performance_metrics_collection.find(
            {},
            {"_id": 0}
        ).sort(
            "search_count",
            -1
        ).limit(3)

    )

    return {

        "status": "success",

        "count": len(algorithms),

        "data": algorithms

    }
# ============================================================
# RECENT SEARCHES
# ============================================================

@router.get("/dashboard/recent-searches")
def recent_searches():

    searches = list(

        query_history_collection.find(
            {},
            {"_id": 0}
        ).sort(
            "timestamp",
            -1
        ).limit(10)

    )

    return {

        "status": "success",

        "count": len(searches),

        "data": searches

    }
    # ============================================================
# API USAGE
# ============================================================

@router.get("/dashboard/api-usage")
def api_usage():

    pipeline = [

        {
            "$group": {

                "_id": "$endpoint",

                "count": {

                    "$sum": 1

                }

            }

        },

        {

            "$sort": {

                "count": -1

            }

        }

    ]

    result = list(

        api_log_collection.aggregate(

            pipeline

        )

    )

    return {

        "status": "success",

        "data": result

    }
# ============================================================
# GENERATION ANALYTICS
# ============================================================

@router.get("/dashboard/generation-analytics")
def generation_analytics():

    generated = generation_log_collection.count_documents({
        "status": "generated"
    })

    retrieved = generation_log_collection.count_documents({
        "status": "retrieved"
    })

    failed = generation_log_collection.count_documents({
        "status": "failed"
    })

    return {

        "status": "success",

        "data": {

            "generated": generated,

            "retrieved": retrieved,

            "failed": failed

        }

    }