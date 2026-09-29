import requests, json

print("=========================================================================")
print("        AI-POWERED ALGORITHM GENERATION USING REINFORCEMENT LEARNING     ")
print("                           LIVE OUTPUT REPORT                            ")
print("=========================================================================")

# Health Check
r_health = requests.get("http://127.0.0.1:8000/health").json()
print(f"[SYSTEM STATUS] Backend: {r_health.get('backend')} | MongoDB: {r_health.get('mongodb')} | Overall: {r_health.get('status')}")

# Algorithm Query
r_search = requests.get("http://127.0.0.1:8000/algorithm/Kadane's%20Algorithm").json()
print(f"\n[SEARCH TEST] Query: Kadane's Algorithm")
print(f"  - Found Status: {r_search.get('status')}")
print(f"  - Data Source:  {r_search.get('source')} (Response Time: {r_search.get('response_time_ms')} ms)")
algo = r_search.get('data', {})
print(f"  - Category:     {algo.get('category')}")
print(f"  - Complexity:   Time {algo.get('time_complexity')} | Space {algo.get('space_complexity')}")

# GA-RL Generation
print(f"\n[REINFORCEMENT LEARNING ENGINE] Generating & Optimizing 'Dijkstra Algorithm'...")
r_garl = requests.post("http://127.0.0.1:8000/garl/generate", json={"algorithm_name": "Dijkstra Algorithm", "category": "Graph"}).json()
garl_data = r_garl.get("data", {})
meta = garl_data.get("garl_metadata", {})
print(f"  - Engine:               {r_garl.get('engine')}")
print(f"  - Latency:              {r_garl.get('response_time_ms')} ms")
print(f"  - Best Strategy:        {meta.get('best_strategy')}")
print(f"  - Baseline Accuracy:    {meta.get('baseline_accuracy')}%")
print(f"  - Achieved Accuracy:    {meta.get('achieved_accuracy')}%")
print(f"  - Accuracy Gain:        +{meta.get('accuracy_improvement')}%")
print(f"  - Q-Learning Reward:    {meta.get('total_reward')}")

# Statistics & Dashboard
r_stats = requests.get("http://127.0.0.1:8000/statistics").json()
s = r_stats.get("statistics", {})
print(f"\n[DASHBOARD METRICS]")
print(f"  - Total Algorithms in DB: {s.get('total_algorithms')}")
print(f"  - Total Queries Handled:  {s.get('total_queries')}")
print(f"  - MongoDB Hits:           {s.get('found_queries')}")
print(f"  - Total Generations:      {s.get('total_generations')}")

# Frontend verification
r_fe = requests.get("http://localhost:3000")
print(f"\n[FRONTEND PORTAL] Running on http://localhost:3000 (HTTP Status: {r_fe.status_code} OK)")
print("=========================================================================")
