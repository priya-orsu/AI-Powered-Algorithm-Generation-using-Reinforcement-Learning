from pymongo import MongoClient
from dotenv import load_dotenv
import os

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "AlgorithmGenerator")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "algorithms")

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

# Hybrid GA-RL Collections
garl_logs_collection = db["garl_logs"]
garl_qtable_collection = db["garl_qtable"]
garl_benchmark_collection = db["garl_benchmarks"]

# User & Authentication Collections
users_collection = db["users"]
otp_requests_collection = db["otp_requests"]

# ==========================================================
# MongoDB Indexes
# ==========================================================

algorithm_collection.create_index("algorithm_name")
algorithm_collection.create_index("category")
algorithm_collection.create_index("keywords")

performance_metrics_collection.create_index("algorithm_name")

query_history_collection.create_index("query")

generation_log_collection.create_index("algorithm_name")

garl_logs_collection.create_index("algorithm_name")
garl_benchmark_collection.create_index("algorithm_name")

users_collection.create_index("username", unique=True)
users_collection.create_index("email")
otp_requests_collection.create_index("identifier")
otp_requests_collection.create_index("expires_at", expireAfterSeconds=0)

# ==========================================================
# Connection Status
# ==========================================================

print("[SUCCESS] Connected to MongoDB Successfully!")