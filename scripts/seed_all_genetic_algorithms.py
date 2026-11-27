import time
from app.database.connection import algorithm_collection, query_history_collection, generation_log_collection
from app.services.hybrid_garl import hybrid_garl_engine
from app.services.genetic_algorithms_catalog import GENETIC_ALGORITHMS_REGISTRY
from datetime import datetime

print("=========================================================================")
print("          SEEDING ADVANCED GENETIC ALGORITHMS INTO MONGODB               ")
print("=========================================================================")

seeded_count = 0
for item in GENETIC_ALGORITHMS_REGISTRY:
    name = item["algorithm_name"]
    category = item["category"]
    print(f"\n[OPTIMIZING & PERSISTING] {name} ({category})...")

    # Run GA-RL generation and optimization
    start_t = time.time()
    res = hybrid_garl_engine.generate_and_optimize(name, category)
    doc = res["document"]
    elapsed_ms = round((time.time() - start_t) * 1000, 2)

    # Upsert into MongoDB
    algorithm_collection.update_one(
        {"algorithm_name": {"$regex": f"^{name}$", "$options": "i"}},
        {"$set": doc},
        upsert=True
    )

    # Log into query history & generation logs
    query_history_collection.insert_one({
        "query": name,
        "search_type": "GA-RL Engine Seed",
        "status": f"GA-RL Optimized ({doc['garl_metadata']['achieved_accuracy']}%)",
        "timestamp": datetime.now()
    })

    generation_log_collection.insert_one({
        "algorithm_name": name,
        "status": "garl_optimized",
        "source": "Hybrid GA-RL Engine",
        "accuracy": doc["garl_metadata"]["achieved_accuracy"],
        "timestamp": datetime.now()
    })

    seeded_count += 1
    print(f"  -> Successfully Seeded! Accuracy: {doc['garl_metadata']['achieved_accuracy']}% | Strategy: {doc['garl_metadata']['best_strategy']} | Latency: {elapsed_ms}ms")

print(f"\n[DONE] Successfully seeded {seeded_count} Genetic Algorithms into MongoDB database!")
total_algos = algorithm_collection.count_documents({})
print(f"[STATUS] Total Algorithms now in MongoDB collection: {total_algos}")
