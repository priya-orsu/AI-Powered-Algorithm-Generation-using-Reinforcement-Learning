from pymongo import MongoClient
from dotenv import load_dotenv
import os

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# ==========================================================
# MongoDB Connection
# ==========================================================

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

# ==========================================================
# Collections
# ==========================================================

# Main Algorithms Collection
algorithm_collection = db[COLLECTION_NAME]

# User Search History
query_history_collection = db["query_history"]

# AI Generation Logs
generation_log_collection = db["generation_logs"]

# API Logs
api_log_collection = db["api_logs"]

# Performance Metrics
performance_metrics_collection = db["performance_metrics"]

# ==========================================================
# MongoDB Indexes
# ==========================================================

algorithm_collection.create_index("algorithm_name")
algorithm_collection.create_index("category")
algorithm_collection.create_index("keywords")

performance_metrics_collection.create_index("algorithm_name")

query_history_collection.create_index("query")

generation_log_collection.create_index("algorithm_name")

# ==========================================================
# Connection Status
# ==========================================================

print("✅ Connected to MongoDB Successfully!")