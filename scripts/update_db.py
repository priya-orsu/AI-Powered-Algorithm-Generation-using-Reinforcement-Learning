import os
import sys
from app.database.connection import algorithm_collection
from app.services.hybrid_garl import hybrid_garl_engine

def update_all_algorithms():
    # Ensure Kadane's Algorithm exists in MongoDB
    kadane_doc = algorithm_collection.find_one({"algorithm_name": {"$regex": "kadane", "$options": "i"}})
    if not kadane_doc:
        print("Inserting Kadane's Algorithm into MongoDB...")
        res = hybrid_garl_engine.generate_and_optimize("Kadane's Algorithm", "Dynamic Programming")
        algorithm_collection.insert_one(res["document"])

    algorithms = list(algorithm_collection.find({}))
    print(f"Found {len(algorithms)} algorithms in MongoDB collection.")

    for algo in algorithms:
        name = algo.get("algorithm_name")
        category = algo.get("category", "General")
        if not name:
            continue
        
        print(f"Updating algorithm document for: '{name}'...")
        res = hybrid_garl_engine.generate_and_optimize(name, category)
        updated_doc = res["document"]
        
        algorithm_collection.update_one(
            {"_id": algo["_id"]},
            {"$set": {
                "working_steps": updated_doc["working_steps"],
                "python_code": updated_doc["python_code"],
                "pseudocode": updated_doc["pseudocode"],
                "advantages": updated_doc["advantages"],
                "disadvantages": updated_doc["disadvantages"],
                "sample_questions": updated_doc["sample_questions"]
            }}
        )

    print("\n[SUCCESS] All MongoDB algorithm documents updated successfully!")

if __name__ == "__main__":
    update_all_algorithms()

