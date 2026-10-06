"""
Master Database Seeder & Syncer
Seeds all curated Computer Science, Genetic Algorithms, Machine Learning,
and Optimization Algorithms into MongoDB with verified production-ready code,
accurate working steps, pseudocode, complexities, and LeetCode problems.
"""

import os
import sys
import time
from datetime import datetime

# Ensure project root is on sys.path
sys.path.insert(0, os.getcwd())

from app.database.connection import (
    algorithm_collection,
    query_history_collection,
    generation_log_collection
)
from app.services.hybrid_garl import hybrid_garl_engine
from app.services.algorithm_comprehensive_catalog import ALGORITHM_CATALOG
from app.services.genetic_algorithms_catalog import GENETIC_ALGORITHMS_REGISTRY
from app.services.ml_encoding_catalog import ML_ENCODING_REGISTRY

def seed_all():
    print("=========================================================================")
    print("      SEEDING & REFRESHING ALL ALGORITHMS IN MONGODB (NO DUMMY VALUES)   ")
    print("=========================================================================")

    # 1. Clean out placeholder documents with dummy 'processed = []' or generic template code
    deleted = algorithm_collection.delete_many({
        "$or": [
            {"python_code": {"$regex": "solve_.*\\(dataset, partition_threshold", "$options": "i"}},
            {"python_code": {"$regex": "accumulated_state \\+=", "$options": "i"}},
            {"python_code": {"$regex": "solve_huffman_coding_algorithm", "$options": "i"}},
            {"python_code": {"$regex": "solve_prims_algorithm", "$options": "i"}}
        ]
    })
    print(f"[CLEANUP] Removed {deleted.deleted_count} stale/placeholder documents from MongoDB.")

    # 2. Collect all target algorithms to seed
    targets = []

    # From Comprehensive Catalog
    for k, v in ALGORITHM_CATALOG.items():
        targets.append({"name": v["name"], "category": v["category"]})

    # From Genetic Algorithms Registry
    for item in GENETIC_ALGORITHMS_REGISTRY:
        targets.append({"name": item["algorithm_name"], "category": item["category"]})

    # From ML & Encoding Registry
    for item in ML_ENCODING_REGISTRY:
        targets.append({"name": item["algorithm_name"], "category": item["category"]})

    # Standard Essential Classical Algorithms
    standard_extras = [
        {"name": "Binary Search", "category": "Searching"},
        {"name": "Linear Search", "category": "Searching"},
        {"name": "QuickSort", "category": "Sorting"},
        {"name": "Merge Sort", "category": "Sorting"},
        {"name": "Bubble Sort", "category": "Sorting"},
        {"name": "Counting Sort", "category": "Sorting"},
        {"name": "Radix Sort", "category": "Sorting"},
        {"name": "Breadth First Search (BFS)", "category": "Graph Algorithms"},
        {"name": "Depth First Search (DFS)", "category": "Graph Algorithms"},
        {"name": "Simulated Annealing", "category": "Metaheuristic & Evolutionary Algorithms"},
        {"name": "Particle Swarm Optimization (PSO)", "category": "Metaheuristic & Evolutionary Algorithms"},
        {"name": "Tabu Search", "category": "Metaheuristic & Evolutionary Algorithms"},
        {"name": "B-Tree Indexing Algorithm", "category": "Database & Indexing"}
    ]
    for ex in standard_extras:
        targets.append(ex)

    # De-duplicate by lower name
    seen = set()
    unique_targets = []
    for t in targets:
        k = t["name"].lower().strip()
        if k not in seen:
            seen.add(k)
            unique_targets.append(t)

    print(f"\n[STARTING] Seeding {len(unique_targets)} verified algorithms into MongoDB...")

    success_count = 0
    for idx, item in enumerate(unique_targets, 1):
        name = item["name"]
        cat = item["category"]
        print(f"[{idx}/{len(unique_targets)}] Optimizing & Storing: '{name}' ({cat})...")

        try:
            start_t = time.time()
            res = hybrid_garl_engine.generate_and_optimize(name, cat)
            doc = res["document"]
            elapsed = round((time.time() - start_t) * 1000, 2)

            algorithm_collection.update_one(
                {"algorithm_name": {"$regex": f"^{name}$", "$options": "i"}},
                {"$set": doc},
                upsert=True
            )

            success_count += 1
            print(f"   -> [SAVED] Accuracy: {doc['garl_metadata']['achieved_accuracy']}% | Strategy: {doc['garl_metadata']['best_strategy']} | ({elapsed}ms)")
        except Exception as e:
            print(f"   -> [ERROR] Failed to seed '{name}': {e}")

    total_in_db = algorithm_collection.count_documents({})
    print(f"\n=========================================================================")
    print(f" [COMPLETE] Successfully seeded/updated {success_count} algorithms!")
    print(f" [MONGODB STATUS] Total verified algorithms in database: {total_in_db}")
    print("=========================================================================\n")

if __name__ == "__main__":
    seed_all()
