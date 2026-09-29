import random
import math
import time
from typing import List, Dict, Any, Tuple

class SimulatedAnnealingOptimizer:
    """
    Simulated Annealing (SA) Metaheuristic Optimizer.
    Models physical cooling of metals to avoid local optima in strategy parameter space.
    Accepts worse solutions with probability P = exp(-ΔE / T).
    """
    def __init__(self, initial_temp: float = 100.0, cooling_rate: float = 0.85, min_temp: float = 0.01):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp

    def optimize(self, base_strategy: Dict[str, Any]) -> Dict[str, Any]:
        current = dict(base_strategy)
        current_cost = self._calculate_cost(current)
        best = dict(current)
        best_cost = current_cost
        
        temp = self.initial_temp
        sa_logs = []

        step = 0
        while temp > self.min_temp and step < 20:
            step += 1
            neighbor = dict(current)
            # Perturb parameters
            neighbor["heuristic_weight"] = min(0.99, max(0.5, round(neighbor["heuristic_weight"] + random.uniform(-0.08, 0.08), 2)))
            neighbor["partition_threshold"] = min(50, max(5, neighbor["partition_threshold"] + random.randint(-5, 5)))
            
            neighbor_cost = self._calculate_cost(neighbor)
            delta_e = neighbor_cost - current_cost

            # Acceptance probability
            if delta_e < 0 or random.random() < math.exp(-delta_e / max(temp, 0.001)):
                current = neighbor
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best = dict(current)
                    best_cost = current_cost

            sa_logs.append({
                "step": step,
                "temperature": round(temp, 2),
                "current_cost": round(current_cost, 4),
                "best_cost": round(best_cost, 4),
                "accepted": delta_e < 0 or random.random() < math.exp(-delta_e / max(temp, 0.001))
            })

            temp *= self.cooling_rate

        best["sa_logs"] = sa_logs
        best["sa_best_cost"] = round(best_cost, 4)
        return best

    def _calculate_cost(self, strategy: Dict[str, Any]) -> float:
        # Cost function (inverse of accuracy & efficiency)
        acc = strategy.get("accuracy", 90.0)
        heuristic = strategy.get("heuristic_weight", 0.7)
        cost = (100.0 - acc) + (1.0 - heuristic) * 10.0
        return max(0.1, cost)


class ParticleSwarmOptimizer:
    """
    Particle Swarm Optimization (PSO) Metaheuristic.
    Simulates swarm behavior (birds/fish) to adjust candidate velocity vectors
    towards Personal Best (P_best) and Global Best (G_best).
    """
    def __init__(self, num_particles: int = 6, iterations: int = 10, w: float = 0.5, c1: float = 1.5, c2: float = 1.5):
        self.num_particles = num_particles
        self.iterations = iterations
        self.w = w    # Inertia weight
        self.c1 = c1  # Cognitive coefficient
        self.c2 = c2  # Social coefficient

    def optimize(self, algorithm_name: str) -> Dict[str, Any]:
        particles = []
        for i in range(self.num_particles):
            pos_weight = round(random.uniform(0.60, 0.95), 2)
            pos_thresh = random.randint(10, 40)
            vel_weight = round(random.uniform(-0.05, 0.05), 2)
            vel_thresh = random.randint(-3, 3)

            particle = {
                "id": f"pso_particle_{i+1}",
                "algorithm_name": algorithm_name,
                "position_weight": pos_weight,
                "position_thresh": pos_thresh,
                "velocity_weight": vel_weight,
                "velocity_thresh": vel_thresh,
                "pbest_weight": pos_weight,
                "pbest_thresh": pos_thresh,
                "pbest_fitness": 0.0,
                "fitness": 0.0
            }
            particles.append(particle)

        gbest_fitness = -1.0
        gbest_position = dict(particles[0])

        pso_history = []

        for it in range(1, self.iterations + 1):
            for p in particles:
                # Evaluate fitness
                fit = (p["position_weight"] * 60.0) + (p["position_thresh"] * 0.8) + (10.0 if p.get("cache_enabled", True) else 0.0)
                p["fitness"] = round(fit, 2)

                if fit > p["pbest_fitness"]:
                    p["pbest_fitness"] = fit
                    p["pbest_weight"] = p["position_weight"]
                    p["pbest_thresh"] = p["position_thresh"]

                if fit > gbest_fitness:
                    gbest_fitness = fit
                    gbest_position = dict(p)

            # Update velocity and position
            for p in particles:
                r1, r2 = random.random(), random.random()
                p["velocity_weight"] = self.w * p["velocity_weight"] + self.c1 * r1 * (p["pbest_weight"] - p["position_weight"]) + self.c2 * r2 * (gbest_position["position_weight"] - p["position_weight"])
                p["position_weight"] = min(0.99, max(0.50, round(p["position_weight"] + p["velocity_weight"], 2)))

            pso_history.append({
                "iteration": it,
                "gbest_fitness": round(gbest_fitness, 2),
                "gbest_weight": gbest_position["position_weight"],
                "gbest_thresh": gbest_position["position_thresh"]
            })

        return {
            "gbest_particle": gbest_position,
            "gbest_fitness": round(gbest_fitness, 2),
            "pso_history": pso_history
        }


class TabuSearchOptimizer:
    """
    Tabu Search Metaheuristic.
    Uses flexible memory (Tabu List) to prevent recycling recent search moves.
    """
    def __init__(self, tabu_tenure: int = 4):
        self.tabu_tenure = tabu_tenure

    def optimize(self, initial_solution: Dict[str, Any]) -> Dict[str, Any]:
        current = dict(initial_solution)
        best = dict(current)
        tabu_list: List[str] = []

        ts_logs = []
        for step in range(1, 8):
            move = f"move_w_{random.randint(1, 10)}"
            if move not in tabu_list:
                tabu_list.append(move)
                if len(tabu_list) > self.tabu_tenure:
                    tabu_list.pop(0)

                current["heuristic_weight"] = min(0.99, round(current.get("heuristic_weight", 0.8) + random.uniform(-0.02, 0.03), 2))
                best = dict(current)

            ts_logs.append({
                "step": step,
                "move": move,
                "tabu_list_size": len(tabu_list),
                "current_weight": current["heuristic_weight"]
            })

        best["tabu_logs"] = ts_logs
        return best


class MetaheuristicLearningEngine:
    """
    Unified Metaheuristic Learning Controller combining SA, PSO, and Tabu Search
    to initialize optimal parameter bounds for Genetic Algorithms + RL.
    """
    def __init__(self):
        self.sa = SimulatedAnnealingOptimizer()
        self.pso = ParticleSwarmOptimizer()
        self.ts = TabuSearchOptimizer()

    def run_metaheuristic_optimization(self, algorithm_name: str, base_candidate: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()

        # Run SA optimization
        sa_result = self.sa.optimize(base_candidate)

        # Run PSO swarm search
        pso_result = self.pso.optimize(algorithm_name)

        # Run Tabu Search neighborhood refinement
        ts_result = self.ts.optimize(sa_result)

        exec_time = round((time.time() - start_time) * 1000, 2)

        return {
            "optimized_candidate": ts_result,
            "sa_logs": sa_result.get("sa_logs", []),
            "pso_gbest": pso_result["gbest_particle"],
            "pso_history": pso_result["pso_history"],
            "tabu_logs": ts_result.get("tabu_logs", []),
            "metaheuristic_summary": {
                "algorithm": "Simulated Annealing + Particle Swarm + Tabu Search",
                "execution_time_ms": exec_time,
                "initial_temperature": 100.0,
                "cooling_rate": 0.85,
                "swarm_size": 6,
                "pso_gbest_fitness": pso_result["gbest_fitness"]
            }
        }

metaheuristic_engine = MetaheuristicLearningEngine()
