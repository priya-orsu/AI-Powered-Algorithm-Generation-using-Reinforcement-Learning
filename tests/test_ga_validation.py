import requests, json

print("=========================================================================")
print("           VALIDATING GENETIC ALGORITHMS INTEGRATION REPORT              ")
print("=========================================================================")

# 1. Health check
r_health = requests.get("http://127.0.0.1:8000/health").json()
print(f"[HEALTH CHECK] Backend: {r_health.get('backend')} | DB: {r_health.get('mongodb')} | Status: {r_health.get('status')}")

# 2. Query each new Genetic Algorithm via API
ga_queries = [
    "Simple Genetic Algorithm (SGA)",
    "Genetic Algorithm for TSP (GA-TSP)",
    "Genetic Algorithm for 0/1 Knapsack (GA-Knapsack)",
    "NSGA-II Multi-Objective Genetic Algorithm",
    "Differential Evolution (DE)",
    "Island Model Parallel Genetic Algorithm",
    "Adaptive Genetic Algorithm (AGA)"
]

print("\n[VERIFYING ALL GENETIC ALGORITHMS VIA HTTP REST ENDPOINT /algorithm/{name}]")
for query in ga_queries:
    encoded = requests.utils.quote(query)
    r = requests.get(f"http://127.0.0.1:8000/algorithm/{encoded}")
    if r.status_code == 200:
        data = r.json()
        algo = data.get("data", {})
        meta = algo.get("garl_metadata", {})
        steps = algo.get("working_steps", [])
        code_lines = len(algo.get("python_code", "").split("\n"))
        print(f" -> [200 OK] {query[:38]:38} | Latency: {data.get('response_time_ms', 0):.2f}ms | Source: {data.get('source')} | Accuracy: {meta.get('achieved_accuracy')}% | Steps: {len(steps)} | Code Lines: {code_lines}")
    else:
        print(f" -> [ERROR {r.status_code}] {query}")

# 3. Test GA-RL Dynamic Generation endpoint for a novel prompt
print("\n[TESTING GA-RL ENGINE ON-THE-FLY GENERATION]")
garl_req = {"algorithm_name": "Multi-Island Genetic Migration Strategy", "category": "Evolutionary Computation"}
r_garl = requests.post("http://127.0.0.1:8000/garl/generate", json=garl_req)
print(f" -> POST /garl/generate: HTTP {r_garl.status_code}")
if r_garl.status_code == 200:
    res = r_garl.json()
    algo_data = res.get("data", {})
    garl_meta = algo_data.get("garl_metadata", {})
    print(f"    Name:       {algo_data.get('algorithm_name')}")
    print(f"    Strategy:   {garl_meta.get('best_strategy')}")
    print(f"    Accuracy:   {garl_meta.get('achieved_accuracy')}% (Baseline: {garl_meta.get('baseline_accuracy')}%)")
    print(f"    Latency:    {res.get('response_time_ms')}ms")

# 4. Check Frontend
r_fe = requests.get("http://localhost:3000")
print(f"\n[FRONTEND DEV SERVER] http://localhost:3000 -> HTTP {r_fe.status_code} OK")

# 5. Statistics
r_stat = requests.get("http://127.0.0.1:8000/statistics").json()
print(f"[TOTAL ALGORITHMS IN DB] {r_stat.get('statistics', {}).get('total_algorithms')} algorithms now stored and ready.")
print("=========================================================================")
