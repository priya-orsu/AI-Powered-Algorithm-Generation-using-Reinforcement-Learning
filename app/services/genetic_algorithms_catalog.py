"""
Genetic Algorithms & Evolutionary Computation Catalog
Comprehensive implementations, mathematical working steps, pseudocode,
complexities, advantages, disadvantages, and interview questions.
"""
from typing import List, Dict, Any

GENETIC_ALGORITHMS_REGISTRY = [
    {
        "algorithm_name": "Simple Genetic Algorithm (SGA)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "description": "Foundational binary-encoded genetic algorithm implementing Holland's schema theorem, fitness-proportionate roulette wheel selection, single-point crossover, and bit-flip mutation for global multimodal function optimization.",
        "problem_statement": "Optimize a continuous non-linear mathematical objective function f(x) over a bounded interval using binary chromosome encoding and evolutionary mechanics.",
        "keywords": ["Simple Genetic Algorithm", "SGA", "Roulette Wheel Selection", "Binary Chromosome", "Single Point Crossover", "Holland Schema", "Evolutionary Algorithm"]
    },
    {
        "algorithm_name": "Genetic Algorithm for TSP (GA-TSP)",
        "category": "Combinatorial Optimization",
        "description": "Permutation-based genetic algorithm designed to solve the NP-hard Traveling Salesperson Problem by finding the minimum Euclidean tour visiting N cities exactly once using Ordered Crossover (OX) and Inversion Mutation.",
        "problem_statement": "Find the shortest possible closed tour visiting each of N cities exactly once and returning to the starting point.",
        "keywords": ["GA-TSP", "Traveling Salesperson Problem", "Ordered Crossover", "OX", "Inversion Mutation", "Permutation Encoding", "Route Optimization", "NP-Hard"]
    },
    {
        "algorithm_name": "Genetic Algorithm for 0/1 Knapsack (GA-Knapsack)",
        "category": "Constrained Optimization",
        "description": "Constraint-handling genetic algorithm for the 0/1 Knapsack problem using dynamic penalty coefficients for infeasible over-capacity weight configurations, uniform crossover, and elitism preservation.",
        "problem_statement": "Maximize total profit value of packed items subject to a strict maximum weight capacity limit W using binary inclusion genes.",
        "keywords": ["GA-Knapsack", "0/1 Knapsack", "Constraint Penalty", "Combinatorial Optimization", "Dynamic Penalty Function", "Tournament Selection", "Elitism"]
    },
    {
        "algorithm_name": "NSGA-II Multi-Objective Genetic Algorithm",
        "category": "Multi-Objective Optimization",
        "description": "Elite state-of-the-art multi-objective evolutionary algorithm employing fast non-dominated sorting O(M*N^2), crowding distance diversity preservation, and constrained Pareto-optimal frontier generation without user-defined niche parameters.",
        "problem_statement": "Simultaneously optimize multiple conflicting objective functions f1(x) and f2(x) to approximate the global Pareto-optimal frontier.",
        "keywords": ["NSGA-II", "Multi-Objective Optimization", "Pareto Frontier", "Fast Non-Dominated Sorting", "Crowding Distance", "Deb Algorithm", "Evolutionary Multi-Criterion"]
    },
    {
        "algorithm_name": "Differential Evolution (DE)",
        "category": "Evolutionary Computation",
        "description": "Stochastically robust population-based continuous parameter optimizer that mutates individuals using scaled vector differences between randomly sampled candidates (DE/rand/1/bin) followed by binomial crossover and greedy survivor selection.",
        "problem_statement": "Find the global minimum of a non-differentiable, non-linear continuous objective function f(x) in D-dimensional real space R^D.",
        "keywords": ["Differential Evolution", "DE", "Vector Difference Mutation", "DE/rand/1/bin", "Continuous Optimization", "Storn and Price", "Global Optimization"]
    },
    {
        "algorithm_name": "Island Model Parallel Genetic Algorithm",
        "category": "Distributed Evolutionary Algorithms",
        "description": "Coarse-grained parallel genetic algorithm partitioning the global population into isolated sub-populations (islands) that evolve independently with periodic migration of elite chromosomes across a ring topology to preserve diversity and eliminate premature convergence.",
        "problem_statement": "Scale evolutionary search across multi-core distributed architectures while avoiding premature convergence in complex multimodal fitness landscapes.",
        "keywords": ["Island Model", "Parallel Genetic Algorithm", "Subpopulation Migration", "Ring Topology", "Coarse-Grained GA", "Premature Convergence Prevention", "Distributed Computing"]
    },
    {
        "algorithm_name": "Adaptive Genetic Algorithm (AGA)",
        "category": "Self-Adaptive Optimization",
        "description": "Dynamically regulated evolutionary algorithm implementing the Srinivas-Patnaik formulation to automatically adjust crossover probability Pc and mutation probability Pm in real-time according to individual fitness relative to population variance.",
        "problem_statement": "Dynamically maintain an optimal balance between global exploration and local exploitation throughout generations without manual hyperparameter tuning.",
        "keywords": ["Adaptive Genetic Algorithm", "AGA", "Dynamic Crossover", "Adaptive Mutation", "Srinivas-Patnaik", "Self-Adaptive Parameterization", "Exploration Exploitation Balance"]
    }
]

def is_genetic_algorithm(algorithm_name: str) -> bool:
    name = algorithm_name.lower().strip()
    ga_identifiers = [
        'genetic', 'ga-', 'sga', 'nsga', 'differential evolution',
        'island model', 'adaptive genetic', 'knapsack genetic', 'ga_knapsack',
        'tsp genetic', 'ga_tsp', 'evolutionary', 'de/rand', 'chromosom'
    ]
    return any(identifier in name for identifier in ga_identifiers)

def get_matched_ga_key(algorithm_name: str) -> str:
    name = algorithm_name.lower().strip()
    if 'nsga' in name or 'multi-objective' in name or 'pareto' in name:
        return 'nsga_ii'
    elif 'tsp' in name or 'traveling' in name or 'salesperson' in name or 'tour' in name:
        return 'ga_tsp'
    elif 'knapsack' in name or 'backpack' in name or '0/1' in name:
        return 'ga_knapsack'
    elif 'differential evolution' in name or 'de/rand' in name or 'difference vector' in name:
        return 'differential_evolution'
    elif 'island' in name or 'parallel genetic' in name or 'migration' in name:
        return 'island_ga'
    elif 'adaptive' in name or 'aga' in name or 'srinivas' in name:
        return 'adaptive_ga'
    else:
        return 'simple_ga'

def get_ga_working_steps(algorithm_name: str) -> List[str]:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return [
            "Start",
            "Read city coordinate array C of size N and GA hyperparameters (Population P, Generations G, Mutation Rate p_m).",
            "Compute pairwise Euclidean distance matrix D where D[i,j] = hypot(C[i].x - C[j].x, C[i].y - C[j].y).",
            "Initialize population with P random valid city permutations (tours) of length N.",
            "For generation g = 1 to G, do:",
            "  Evaluate Tour Length for each individual: L = sum(D[tour[k], tour[(k+1)%N]]) for k = 0 to N - 1.",
            "  Calculate Fitness F = 1.0 / (L + 1e-6).",
            "  Select top 2 elite tours and preserve unchanged into next-generation population.",
            "  While next-generation size < P, do:",
            "    Select two parent tours p1 and p2 using 3-way Tournament Selection.",
            "    Apply Ordered Crossover (OX): Select random slice [a, b] from p1; copy segment to child; fill remaining slots with unused cities from p2 in relative order.",
            "    Apply Inversion Mutation with probability p_m: Reverse a random sub-tour segment [i, j].",
            "    Add child tour to next generation.",
            "  Update population = next-generation.",
            "Return best tour permutation and minimum total Euclidean tour length.",
            "Stop"
        ]
    elif key == "ga_knapsack":
        return [
            "Start",
            "Read item weights array W, item values array V, knapsack capacity C_max, and population size P.",
            "Initialize population of P binary chromosomes of length N where gene = 1 if item is included, 0 otherwise.",
            "For generation g = 1 to G, do:",
            "  For each chromosome, calculate Total Weight = sum(chrom[i] * W[i]) and Total Value = sum(chrom[i] * V[i]).",
            "  Evaluate Fitness with dynamic penalty: If Total Weight > C_max, Fitness = max(0, Total Value - PenaltyCoeff * (Total Weight - C_max)); Else Fitness = Total Value.",
            "  Sort population by fitness in descending order and retain top elite individuals.",
            "  Select mating parents using Tournament Selection.",
            "  Perform Uniform Crossover with probability p_c: Exchange genes between parents with 50% probability per bit.",
            "  Apply Bit-Flip Mutation with probability p_m: Invert 0 to 1 or 1 to 0 for random genes.",
            "  Form new generation and update global best valid knapsack solution.",
            "Return best binary allocation, total packed value, and total packed weight.",
            "Stop"
        ]
    elif key == "nsga_ii":
        return [
            "Start",
            "Initialize parent population P_0 of size N with random candidate solutions.",
            "Evaluate objective functions f_1(x) and f_2(x) for all individuals in P_0.",
            "Execute Fast Non-Dominated Sort on P_0 to categorize individuals into Pareto Fronts F_1, F_2, ..., F_k.",
            "Calculate Crowding Distance for each individual within its assigned Pareto Front to preserve diversity.",
            "Generate offspring population Q_0 of size N using binary tournament selection, simulated binary crossover (SBX), and polynomial mutation.",
            "For generation t = 0 to G - 1, do:",
            "  Combine parent and offspring populations: R_t = P_t U Q_t (size 2N).",
            "  Execute Fast Non-Dominated Sort on combined population R_t.",
            "  Initialize empty next-generation population P_{t+1}.",
            "  For each front F_i, do:",
            "    If |P_{t+1}| + |F_i| <= N, add all individuals of F_i to P_{t+1} and calculate crowding distances.",
            "    Else, sort F_i using Crowding Comparison Operator (<_n) and append the best (N - |P_{t+1}|) individuals to P_{t+1}.",
            "    Break loop once P_{t+1} has exactly N individuals.",
            "  Generate offspring population Q_{t+1} from P_{t+1} via Crowded Tournament Selection, SBX, and mutation.",
            "Return non-dominated Pareto-optimal solutions from Front F_1.",
            "Stop"
        ]
    elif key == "differential_evolution":
        return [
            "Start",
            "Read problem dimension D, lower/upper bounds, population size NP, differential weight F in [0, 2], and crossover rate CR in [0, 1].",
            "Initialize population P with NP real-valued vectors x_i uniformly distributed within search bounds.",
            "Evaluate objective fitness f(x_i) for each vector in P.",
            "For generation g = 1 to G, do:",
            "  For each target vector x_i in P (i = 1 to NP), do:",
            "    Select three mutually distinct random indices r1, r2, r3 from population such that r1 != r2 != r3 != i.",
            "    Compute donor mutant vector: v_i = x_{r1} + F * (x_{r2} - x_{r3}).",
            "    Clamp mutant vector v_i coordinates within search bounds.",
            "    Generate trial vector u_i via Binomial Crossover:",
            "      Pick a random dimension index j_rand from 1 to D.",
            "      For each dimension j = 1 to D, set u_{i,j} = v_{i,j} if rand(0,1) <= CR or j == j_rand, else u_{i,j} = x_{i,j}.",
            "    Evaluate objective function f(u_i).",
            "    Perform Greedy Selection: If f(u_i) <= f(x_i), replace x_i with u_i in next generation; else retain x_i.",
            "  Update global best vector with minimum objective value.",
            "Return best continuous parameter vector x_best and minimum objective value.",
            "Stop"
        ]
    elif key == "island_ga":
        return [
            "Start",
            "Initialize M independent sub-populations (islands) each containing K individuals across distributed workers.",
            "Define migration interval (every T generations) and migration rate (top R elite individuals).",
            "Establish unidirectional or bidirectional ring migration topology: Island i -> Island (i + 1) % M.",
            "For generation g = 1 to G, do:",
            "  For each island m = 1 to M in parallel, do:",
            "    Evaluate individual fitness within island m.",
            "    Perform standard GA cycle (Selection, Crossover, Mutation, Elitism) on local sub-population.",
            "  If g % T == 0 (Migration Epoch):",
            "    Extract top R elite individuals from each island m.",
            "    Transmit migrant copies to target neighbor island (m + 1) % M.",
            "    Replace R worst individuals on receiving island with incoming migrant solutions.",
            "  Track global elite solution across all islands.",
            "Return global best chromosome across all island sub-populations.",
            "Stop"
        ]
    elif key == "adaptive_ga":
        return [
            "Start",
            "Initialize population of P chromosomes and define base adjustment coefficients k1, k2, k3, k4.",
            "For generation g = 1 to G, do:",
            "  Evaluate fitness f_i for each individual in the population.",
            "  Compute population statistics: Maximum Fitness f_max, Average Fitness f_avg.",
            "  Sort population by fitness and retain top elite chromosomes.",
            "  While forming next generation:",
            "    Select candidate parents p1 and p2.",
            "    Determine higher parent fitness: f_prime = max(f(p1), f(p2)).",
            "    Calculate Adaptive Crossover Rate: If f_prime >= f_avg, P_c = k1 * (f_max - f_prime) / (f_max - f_avg); Else P_c = k2.",
            "    Perform crossover between p1 and p2 with probability P_c to produce child c.",
            "    Evaluate child fitness f_c.",
            "    Calculate Adaptive Mutation Rate: If f_c >= f_avg, P_m = k3 * (f_max - f_c) / (f_max - f_avg); Else P_m = k4.",
            "    Apply gene mutation to child c with adaptive probability P_m.",
            "    Append child to next generation.",
            "  Update population with adaptive offspring.",
            "Return best optimized solution chromosome.",
            "Stop"
        ]
    else:
        return [
            "Start",
            "Initialize random population of P binary candidate solution chromosomes of bit-length L.",
            "Evaluate objective fitness f(x) for all individuals in the population.",
            "For generation g = 1 to G, do:",
            "  Compute total population fitness sum_f and selection probability p_i = f_i / sum_f.",
            "  Construct cumulative probability distribution for Roulette Wheel Selection.",
            "  Preserve top elite chromosome into next generation.",
            "  While next generation size < P, do:",
            "    Spin roulette wheel to select parent 1 and parent 2.",
            "    Perform Single-Point Crossover with probability p_c: Choose random point k; swap tail segments.",
            "    Perform Bit-Flip Mutation with probability p_m: Invert each bit independently.",
            "    Add offspring to next generation.",
            "  Update population = next generation.",
            "  Track elite chromosome with maximum fitness.",
            "Return elite solution chromosome and decoded optimal parameter value.",
            "Stop"
        ]

def get_ga_python_code(algorithm_name: str) -> str:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return """# Genetic Algorithm for Traveling Salesperson Problem (GA-TSP)
import random
import math

def ga_tsp(num_cities=12, pop_size=50, generations=80, mutation_rate=0.15):
    random.seed(42)
    cities = {i: (random.uniform(5.0, 95.0), random.uniform(5.0, 95.0)) for i in range(num_cities)}

    def euclidean_dist(c1, c2):
        x1, y1 = cities[c1]
        x2, y2 = cities[c2]
        return math.hypot(x1 - x2, y1 - y2)

    def calculate_tour_distance(tour):
        return sum(euclidean_dist(tour[i], tour[(i + 1) % num_cities]) for i in range(num_cities))

    population = [random.sample(range(num_cities), num_cities) for _ in range(pop_size)]
    best_tour = min(population, key=calculate_tour_distance)
    best_distance = calculate_tour_distance(best_tour)

    def ordered_crossover(parent1, parent2):
        a, b = sorted(random.sample(range(num_cities), 2))
        child = [None] * num_cities
        child[a:b+1] = parent1[a:b+1]
        copied = set(child[a:b+1])
        remaining = [city for city in parent2 if city not in copied]
        idx = 0
        for i in range(num_cities):
            if child[i] is None:
                child[i] = remaining[idx]
                idx += 1
        return child

    def inversion_mutation(tour):
        if random.random() < mutation_rate:
            a, b = sorted(random.sample(range(num_cities), 2))
            tour[a:b+1] = reversed(tour[a:b+1])
        return tour

    for gen in range(generations):
        population.sort(key=calculate_tour_distance)
        next_gen = [population[0][:], population[1][:]] # Elitism

        while len(next_gen) < pop_size:
            p1 = min(random.sample(population[:25], 3), key=calculate_tour_distance)
            p2 = min(random.sample(population[:25], 3), key=calculate_tour_distance)
            child = ordered_crossover(p1, p2)
            child = inversion_mutation(child)
            next_gen.append(child)

        population = next_gen
        curr_best = min(population, key=calculate_tour_distance)
        curr_dist = calculate_tour_distance(curr_best)
        if curr_dist < best_distance:
            best_distance = curr_dist
            best_tour = curr_best[:]

    return best_tour, round(best_distance, 2)

optimal_route, min_distance = ga_tsp(num_cities=12, pop_size=50, generations=80)
print(f"[GA-TSP OPTIMAL TOUR] Sequence: {optimal_route}")
print(f"[GA-TSP BENCHMARK] Total Euclidean Tour Distance: {min_distance} km")
"""
    elif key == "ga_knapsack":
        return """# Genetic Algorithm for 0/1 Knapsack with Constraint Penalty Function
import random

def ga_knapsack(capacity=55, pop_size=40, generations=60, mutation_rate=0.08):
    random.seed(42)
    item_weights = [12, 18, 25, 10, 15, 8, 22, 14, 9, 30]
    item_values  = [70, 95, 130, 60, 85, 45, 110, 80, 50, 150]
    num_items = len(item_weights)
    penalty_multiplier = 20.0

    def evaluate(chromosome):
        total_weight = sum(w for b, w in zip(chromosome, item_weights) if b == 1)
        total_value  = sum(v for b, v in zip(chromosome, item_values)  if b == 1)
        violation = max(0, total_weight - capacity)
        fitness = max(0.0, total_value - (violation * penalty_multiplier))
        return fitness, total_weight, total_value

    population = [[random.randint(0, 1) for _ in range(num_items)] for _ in range(pop_size)]
    best_chrom = None
    best_fitness = -1.0

    for gen in range(generations):
        evaluated = [(ind, evaluate(ind)) for ind in population]
        evaluated.sort(key=lambda x: x[1][0], reverse=True)

        if evaluated[0][1][0] > best_fitness and evaluated[0][1][1] <= capacity:
            best_fitness = evaluated[0][1][0]
            best_chrom = evaluated[0][0][:]

        next_gen = [evaluated[0][0][:], evaluated[1][0][:]] # Elitism

        while len(next_gen) < pop_size:
            p1 = max(random.sample(population, 3), key=lambda x: evaluate(x)[0])
            p2 = max(random.sample(population, 3), key=lambda x: evaluate(x)[0])
            child = [p1[i] if random.random() < 0.5 else p2[i] for i in range(num_items)]
            for i in range(num_items):
                if random.random() < mutation_rate:
                    child[i] = 1 - child[i]
            next_gen.append(child)

        population = next_gen

    final_fit, packed_weight, packed_value = evaluate(best_chrom)
    return best_chrom, packed_weight, packed_value

selected_items, total_wt, total_val = ga_knapsack(capacity=55)
print(f"[GA-KNAPSACK SOLUTION] Binary Allocation: {selected_items}")
print(f"[GA-KNAPSACK METRICS] Packed Weight: {total_wt}/55 kg | Total Realized Value: ${total_val}")
"""
    elif key == "nsga_ii":
        return """# NSGA-II: Non-Dominated Sorting Genetic Algorithm II
import random
import math

def nsga_ii(pop_size=30, generations=40):
    random.seed(42)

    def evaluate(x):
        return x**2, (x - 2)**2

    def dominates(p1, p2):
        return (p1["f1"] <= p2["f1"] and p1["f2"] <= p2["f2"]) and (p1["f1"] < p2["f1"] or p1["f2"] < p2["f2"])

    def fast_non_dominated_sort(population):
        fronts = [[]]
        for p in population:
            p["dom_count"] = 0
            p["dominated_set"] = []
            for q in population:
                if dominates(p, q):
                    p["dominated_set"].append(q)
                elif dominates(q, p):
                    p["dom_count"] += 1
            if p["dom_count"] == 0:
                p["rank"] = 1
                fronts[0].append(p)

        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                for q in p["dominated_set"]:
                    q["dom_count"] -= 1
                    if q["dom_count"] == 0:
                        q["rank"] = i + 2
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        return [f for f in fronts if len(f) > 0]

    population = []
    for _ in range(pop_size):
        x = random.uniform(-4.0, 6.0)
        f1, f2 = evaluate(x)
        population.append({"x": round(x, 4), "f1": round(f1, 4), "f2": round(f2, 4)})

    for gen in range(generations):
        offspring = []
        for _ in range(pop_size):
            p1, p2 = random.sample(population, 2)
            child_x = 0.5 * (p1["x"] + p2["x"])
            if random.random() < 0.25:
                child_x += random.gauss(0, 0.4)
            child_x = max(-4.0, min(6.0, child_x))
            f1, f2 = evaluate(child_x)
            offspring.append({"x": round(child_x, 4), "f1": round(f1, 4), "f2": round(f2, 4)})

        combined = population + offspring
        fronts = fast_non_dominated_sort(combined)

        new_pop = []
        for front in fronts:
            if len(new_pop) + len(front) <= pop_size:
                new_pop.extend(front)
            else:
                remaining = pop_size - len(new_pop)
                new_pop.extend(front[:remaining])
                break
        population = new_pop

    pareto_front = [p for p in population if p.get("rank", 1) == 1]
    pareto_front.sort(key=lambda p: p["f1"])
    return pareto_front[:6]

pareto_solutions = nsga_ii(pop_size=30, generations=40)
print(f"[NSGA-II PARETO FRONTIER] Extracted {len(pareto_solutions)} non-dominated trade-off points:")
for idx, sol in enumerate(pareto_solutions):
    print(f"  Point {idx+1}: x = {sol['x']} => f1 (x^2) = {sol['f1']}, f2 ((x-2)^2) = {sol['f2']}")
"""
    elif key == "differential_evolution":
        return """# Differential Evolution (DE/rand/1/bin) Algorithm
import random

def differential_evolution(dimensions=4, pop_size=30, generations=60, F=0.8, CR=0.85):
    random.seed(42)
    bounds = (-10.0, 10.0)

    def objective(x):
        return sum(xi**2 for xi in x)

    population = [[random.uniform(*bounds) for _ in range(dimensions)] for _ in range(pop_size)]
    fitness = [objective(ind) for ind in population]

    for gen in range(generations):
        for i in range(pop_size):
            candidates = [idx for idx in range(pop_size) if idx != i]
            r1, r2, r3 = random.sample(candidates, 3)

            mutant = [
                max(bounds[0], min(bounds[1], population[r1][d] + F * (population[r2][d] - population[r3][d])))
                for d in range(dimensions)
            ]

            rand_dim = random.randint(0, dimensions - 1)
            trial = [
                mutant[d] if random.random() < CR or d == rand_dim else population[i][d]
                for d in range(dimensions)
            ]

            f_trial = objective(trial)
            if f_trial <= fitness[i]:
                population[i] = trial
                fitness[i] = f_trial

    best_idx = fitness.index(min(fitness))
    best_vector = [round(v, 6) for v in population[best_idx]]
    return best_vector, round(fitness[best_idx], 8)

best_coords, min_cost = differential_evolution(dimensions=4)
print(f"[DE GLOBAL MINIMUM] Best Coordinates: {best_coords}")
print(f"[DE RESIDUAL COST] Objective Value sum(x^2): {min_cost}")
"""
    elif key == "island_ga":
        return """# Island Model Parallel Genetic Algorithm with Ring Migration
import random
import math

def island_model_ga(num_islands=4, pop_per_island=20, generations=45, migration_interval=9, migrants_count=2):
    random.seed(42)

    def fitness(chromosome):
        val = int("".join(map(str, chromosome)), 2)
        x = (val / 1023.0) * 10.0 - 5.0
        return 40.0 - (x**2 - 10.0 * math.cos(2 * math.pi * x))

    islands = [[[random.randint(0, 1) for _ in range(10)] for _ in range(pop_per_island)] for _ in range(num_islands)]

    for gen in range(1, generations + 1):
        for island_id in range(num_islands):
            pop = islands[island_id]
            pop.sort(key=fitness, reverse=True)
            next_pop = pop[:2]

            while len(next_pop) < pop_per_island:
                p1, p2 = random.sample(pop[:8], 2)
                split_pt = random.randint(1, 8)
                child = p1[:split_pt] + p2[split_pt:]
                if random.random() < 0.12:
                    bit = random.randint(0, 9)
                    child[bit] = 1 - child[bit]
                next_pop.append(child)
            islands[island_id] = next_pop

        if gen % migration_interval == 0:
            migrants = [islands[i][:migrants_count] for i in range(num_islands)]
            for i in range(num_islands):
                target_island = (i + 1) % num_islands
                islands[target_island][-migrants_count:] = [m[:] for m in migrants[i]]

    all_chroms = [ind for island in islands for ind in island]
    best_chrom = max(all_chroms, key=fitness)
    return best_chrom, round(fitness(best_chrom), 4)

elite_chromosome, max_fitness = island_model_ga(num_islands=4)
print(f"[ISLAND MODEL GA] Global Best Chromosome: {elite_chromosome}")
print(f"[ISLAND MODEL GA] Peak Fitness Score: {max_fitness} across 4 active islands")
"""
    elif key == "adaptive_ga":
        return """# Adaptive Genetic Algorithm (AGA) with Dynamic Crossover & Mutation Probabilities
import random
import math

def adaptive_genetic_algorithm(pop_size=32, bit_len=14, generations=50, k1=1.0, k2=0.5, k3=1.0, k4=0.5):
    random.seed(42)

    def decode(chromosome):
        return int("".join(map(str, chromosome)), 2) / ((1 << bit_len) - 1)

    def fitness(chromosome):
        x = decode(chromosome)
        return max(0.01, math.sin(5 * math.pi * x)**6 * math.exp(-2.0 * math.log(2) * ((x - 0.1) / 0.8)**2))

    population = [[random.randint(0, 1) for _ in range(bit_len)] for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        f_max = max(fitnesses)
        f_avg = sum(fitnesses) / len(fitnesses)

        population.sort(key=fitness, reverse=True)
        next_gen = population[:2]

        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:12], 2)
            f_prime = max(fitness(p1), fitness(p2))

            if f_prime >= f_avg and f_max != f_avg:
                p_c = k1 * (f_max - f_prime) / (f_max - f_avg)
            else:
                p_c = k2
            p_c = max(0.4, min(0.95, p_c))

            if random.random() < p_c:
                cut = random.randint(1, bit_len - 1)
                child = p1[:cut] + p2[cut:]
            else:
                child = p1[:]

            f_child = fitness(child)
            if f_child >= f_avg and f_max != f_avg:
                p_m = k3 * (f_max - f_child) / (f_max - f_avg)
            else:
                p_m = k4
            p_m = max(0.01, min(0.25, p_m))

            for bit in range(bit_len):
                if random.random() < p_m:
                    child[bit] = 1 - child[bit]
            next_gen.append(child)

        population = next_gen

    best_chrom = max(population, key=fitness)
    best_x = round(decode(best_chrom), 5)
    return best_chrom, best_x, round(fitness(best_chrom), 5)

chrom, optimal_param, peak_fitness = adaptive_genetic_algorithm()
print(f"[AGA SOLUTION] Elite Chromosome: {chrom}")
print(f"[AGA OPTIMIZED] Decoded x: {optimal_param} | Max Fitness: {peak_fitness}")
"""
    else:
        return """# Simple Genetic Algorithm (SGA) with Roulette Wheel Selection & Elitism
import random
import math

def simple_genetic_algorithm(pop_size=35, bit_len=16, generations=50, p_c=0.8, p_m=0.03):
    random.seed(42)

    def decode(chromosome):
        val = int("".join(map(str, chromosome)), 2)
        return val / ((1 << bit_len) - 1)

    def fitness(chromosome):
        x = decode(chromosome)
        return max(0.001, x * math.sin(10.0 * math.pi * x) + 1.0)

    population = [[random.randint(0, 1) for _ in range(bit_len)] for _ in range(pop_size)]
    best_chrom = max(population, key=fitness)

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        total_fit = sum(fitnesses)
        probabilities = [f / total_fit for f in fitnesses]

        def roulette_select():
            r = random.random()
            cumulative = 0.0
            for ind, prob in zip(population, probabilities):
                cumulative += prob
                if cumulative >= r:
                    return ind[:]
            return population[-1][:]

        next_gen = [best_chrom[:]]

        while len(next_gen) < pop_size:
            p1, p2 = roulette_select(), roulette_select()
            if random.random() < p_c:
                cut = random.randint(1, bit_len - 1)
                c1 = p1[:cut] + p2[cut:]
                c2 = p2[:cut] + p1[cut:]
            else:
                c1, c2 = p1[:], p2[:]

            for child in (c1, c2):
                for bit in range(bit_len):
                    if random.random() < p_m:
                        child[bit] = 1 - child[bit]
                next_gen.append(child)
                if len(next_gen) >= pop_size:
                    break

        population = next_gen
        curr_best = max(population, key=fitness)
        if fitness(curr_best) > fitness(best_chrom):
            best_chrom = curr_best[:]

    best_x = round(decode(best_chrom), 5)
    return best_chrom, best_x, round(fitness(best_chrom), 5)

elite_gene, decoded_x, max_fit = simple_genetic_algorithm()
print(f"[SGA RESULT] Elite Chromosome: {elite_gene}")
print(f"[SGA OPTIMAL] Optimal Variable x: {decoded_x} | Max Peak Fitness: {max_fit}")
"""

def get_ga_pseudocode(algorithm_name: str) -> str:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return """Algorithm GA_TravelingSalesperson(Cities, PopSize, Generations, p_mut)
Input: Array of city coordinates Cities, Population size PopSize, Iteration count Generations, Mutation probability p_mut
Output: Permutation array representing optimal tour and minimum Euclidean tour length

Begin
    Compute pairwise distance matrix Dist[i, j] for all i, j in Cities
    Population <- InitializeRandomPermutations(PopSize, length(Cities))
    best_tour <- Population[0]
    
    For gen = 1 to Generations do
        For each tour in Population do
            length <- CalculateTourDistance(tour, Dist)
            fitness <- 1.0 / (length + 1e-6)
        End For
        
        Sort Population by fitness in descending order
        NextGen <- [Population[0], Population[1]]  // 2-Elitism
        
        While length(NextGen) < PopSize do
            p1 <- TournamentSelect(Population, k=3)
            p2 <- TournamentSelect(Population, k=3)
            
            // Ordered Crossover (OX) preserving city uniqueness
            [slice_start, slice_end] <- RandomInterval(0, length(Cities) - 1)
            child <- InitializeEmptyArray(length(Cities))
            child[slice_start ... slice_end] <- p1[slice_start ... slice_end]
            FillRemainingSlots(child, p2)
            
            // Inversion Mutation (2-opt reversal)
            If Random(0, 1) < p_mut then
                [rev_a, rev_b] <- RandomInterval(0, length(Cities) - 1)
                ReverseSubArray(child, rev_a, rev_b)
            End If
            
            NextGen.append(child)
        End While
        
        Population <- NextGen
        If TourDistance(Population[0]) < TourDistance(best_tour) then
            best_tour <- Population[0]
        End If
    End For
    
    Return best_tour, TourDistance(best_tour)
End"""
    elif key == "ga_knapsack":
        return """Algorithm GA_Knapsack(Weights, Values, Capacity, PopSize, Generations)
Input: Item weights array Weights, item values array Values, Knapsack limit Capacity, PopSize, Generations
Output: Binary inclusion vector chrom and maximum packed knapsack value

Begin
    N <- length(Weights)
    Population <- RandomBinaryMatrix(PopSize, N)
    best_solution <- EmptyVector()
    best_value <- 0
    
    For gen = 1 to Generations do
        For each chrom in Population do
            tot_w <- Sum(chrom[i] * Weights[i] for i = 0 to N - 1)
            tot_v <- Sum(chrom[i] * Values[i] for i = 0 to N - 1)
            
            // Dynamic Penalty Function for Capacity Overflow
            overflow <- Max(0, tot_w - Capacity)
            fitness <- Max(0, tot_v - PenaltyCoeff * overflow)
        End For
        
        Sort Population by fitness descending
        NextGen <- ElitismPreserve(Population, count=2)
        
        While length(NextGen) < PopSize do
            p1, p2 <- TournamentSelection(Population, size=3)
            child <- UniformCrossover(p1, p2, p_swap=0.5)
            BitFlipMutate(child, p_mut=0.08)
            NextGen.append(child)
        End While
        
        Population <- NextGen
    End For
    
    Return best_solution, TotalValue(best_solution), TotalWeight(best_solution)
End"""
    elif key == "nsga_ii":
        return """Algorithm NSGA_II(Objectives, PopSize, Generations)
Input: Multi-objective functions f1, f2, Population size PopSize, Generations
Output: Pareto-optimal front solutions F_1

Begin
    P_0 <- InitializeRandomPopulation(PopSize)
    EvaluateObjectives(P_0, f1, f2)
    FastNonDominatedSort(P_0)
    CalculateCrowdingDistances(P_0)
    Q_0 <- GenerateOffspring(P_0, PopSize)
    
    For t = 0 to Generations - 1 do
        R_t <- P_t U Q_t  // Combined pool of size 2*PopSize
        Fronts <- FastNonDominatedSort(R_t)
        
        P_{t+1} <- EmptyList()
        i <- 1
        While |P_{t+1}| + |Fronts[i]| <= PopSize do
            AssignCrowdingDistance(Fronts[i])
            P_{t+1}.append(Fronts[i])
            i <- i + 1
        End While
        
        If |P_{t+1}| < PopSize then
            AssignCrowdingDistance(Fronts[i])
            SortByCrowdedComparison(Fronts[i])
            P_{t+1}.append(Fronts[i][0 ... (PopSize - |P_{t+1}|)])
        End If
        
        Q_{t+1} <- MakeOffspring(P_{t+1}, SBX_Crossover, PolynomialMutation)
    End For
    
    Return Fronts[1]  // First Pareto-optimal front
End"""
    elif key == "differential_evolution":
        return """Algorithm DifferentialEvolution(ObjectiveFunc, Dimension, PopSize, Generations, F, CR)
Input: Objective function f, search dimensions Dimension, population PopSize, Generations, scale factor F, crossover CR
Output: Best continuous vector x_best and minimum objective cost

Begin
    Population <- InitializeUniformVectors(PopSize, Dimension, Bounds)
    EvaluateAll(Population, ObjectiveFunc)
    
    For g = 1 to Generations do
        For i = 1 to PopSize do
            r1, r2, r3 <- SampleDistinctIndices(PopSize, exclude=i, count=3)
            v_mutant <- Population[r1] + F * (Population[r2] - Population[r3])
            v_mutant <- ClampToBounds(v_mutant, Bounds)
            
            j_rand <- RandomInteger(1, Dimension)
            trial <- EmptyVector(Dimension)
            For j = 1 to Dimension do
                If Random(0, 1) < CR or j == j_rand then
                    trial[j] <- v_mutant[j]
                Else
                    trial[j] <- Population[i][j]
                End If
            End For
            
            If ObjectiveFunc(trial) <= ObjectiveFunc(Population[i]) then
                Population[i] <- trial
            End If
        End For
    End For
    
    x_best <- FindMinObjectiveVector(Population)
    Return x_best, ObjectiveFunc(x_best)
End"""
    elif key == "island_ga":
        return """Algorithm IslandModelParallelGA(NumIslands, PopPerIsland, Generations, MigInterval, MigCount)
Input: Islands count NumIslands, subpopulation PopPerIsland, Generations, Migration Interval MigInterval, Migrants MigCount
Output: Global elite chromosome across all distributed islands

Begin
    For m = 1 to NumIslands do
        Islands[m] <- InitializeRandomSubPopulation(PopPerIsland)
    End For
    
    For gen = 1 to Generations do
        ParForEach island m in Islands do
            EvolveLocalGA(island, Selection, Crossover, Mutation, Elitism)
        End ParForEach
        
        If gen mod MigInterval = 0 then
            For m = 1 to NumIslands do
                migrants <- ExtractTopElite(Islands[m], MigCount)
                target <- (m mod NumIslands) + 1
                ReplaceWorst(Islands[target], migrants)
            End For
        End If
    End For
    
    Return GlobalBestChromosome(Islands)
End"""
    elif key == "adaptive_ga":
        return """Algorithm AdaptiveGeneticAlgorithm(PopSize, BitLen, Generations, k1, k2, k3, k4)
Input: Population PopSize, gene length BitLen, Generations, adaptation factors k1..k4
Output: Optimally adapted solution chromosome

Begin
    Population <- InitializeRandomPopulation(PopSize, BitLen)
    
    For gen = 1 to Generations do
        EvaluateFitness(Population)
        f_max <- MaxFitness(Population)
        f_avg <- MeanFitness(Population)
        
        NextGen <- Elitism(Population, count=2)
        While length(NextGen) < PopSize do
            p1, p2 <- SelectParents(Population)
            f_prime <- Max(Fitness(p1), Fitness(p2))
            
            If f_prime >= f_avg then
                p_c <- k1 * (f_max - f_prime) / (f_max - f_avg)
            Else
                p_c <- k2
            End If
            
            child <- CrossoverWithProb(p1, p2, p_c)
            
            f_child <- Fitness(child)
            If f_child >= f_avg then
                p_m <- k3 * (f_max - f_child) / (f_max - f_avg)
            Else
                p_m <- k4
            End If
            
            MutateWithProb(child, p_m)
            NextGen.append(child)
        End While
        
        Population <- NextGen
    End For
    
    Return BestIndividual(Population)
End"""
    else:
        return """Algorithm SimpleGeneticAlgorithm(PopSize, BitLen, Generations, p_c, p_m)
Input: Population size PopSize, chromosome length BitLen, Generations, Crossover p_c, Mutation p_m
Output: Optimal chromosome with maximized fitness

Begin
    Population <- InitializeRandomBinaryPopulation(PopSize, BitLen)
    best_chrom <- Population[0]
    
    For gen = 1 to Generations do
        For each ind in Population do
            fitness[ind] <- EvaluateObjective(ind)
        End For
        
        TotalFitness <- Sum(fitness[ind] for ind in Population)
        Probabilities <- [fitness[ind] / TotalFitness for ind in Population]
        
        NextGen <- [best_chrom]
        While length(NextGen) < PopSize do
            p1 <- RouletteWheelSelect(Population, Probabilities)
            p2 <- RouletteWheelSelect(Population, Probabilities)
            
            If Random(0, 1) < p_c then
                point <- RandomInteger(1, BitLen - 1)
                c1 <- p1[0...point] + p2[point...BitLen]
                c2 <- p2[0...point] + p1[point...BitLen]
            Else
                c1, c2 <- p1, p2
            End If
            
            For each child in (c1, c2) do
                For bit = 0 to BitLen - 1 do
                    If Random(0, 1) < p_m then
                        child[bit] <- 1 - child[bit]
                    End If
                End For
                NextGen.append(child)
            End For
        End While
        
        Population <- NextGen
        If MaxFitness(Population) > Fitness(best_chrom) then
            best_chrom <- MaxIndividual(Population)
        End If
    End For
    
    Return best_chrom, Fitness(best_chrom)
End"""

def get_ga_complexity(algorithm_name: str) -> Dict[str, Any]:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return {
            "time_complexity": {"best": "O(G * P * N)", "average": "O(G * P * N^2)", "worst": "O(G * P * N^2)"},
            "space_complexity": "O(P * N)"
        }
    elif key == "ga_knapsack":
        return {
            "time_complexity": {"best": "O(G * P)", "average": "O(G * P * N)", "worst": "O(G * P * N)"},
            "space_complexity": "O(P * N)"
        }
    elif key == "nsga_ii":
        return {
            "time_complexity": {"best": "O(G * M * P^2)", "average": "O(G * M * P^2)", "worst": "O(G * M * P^2)"},
            "space_complexity": "O(M * P)"
        }
    elif key == "differential_evolution":
        return {
            "time_complexity": {"best": "O(G * P * D)", "average": "O(G * P * D)", "worst": "O(G * P * D)"},
            "space_complexity": "O(P * D)"
        }
    elif key == "island_ga":
        return {
            "time_complexity": {"best": "O((G / M) * (P/I * D))", "average": "O((G / M) * (P/I * D) + Mig)", "worst": "O(G * P * D)"},
            "space_complexity": "O(P * D)"
        }
    elif key == "adaptive_ga":
        return {
            "time_complexity": {"best": "O(G * P * L)", "average": "O(G * P * L)", "worst": "O(G * P * L)"},
            "space_complexity": "O(P * L)"
        }
    else:
        return {
            "time_complexity": {"best": "O(G * P)", "average": "O(G * P * L)", "worst": "O(G * P * L)"},
            "space_complexity": "O(P * L)"
        }

def get_ga_advantages(algorithm_name: str) -> List[str]:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return [
            "Effectively circumvents exponential O(N!) factorial brute-force explosion for large routing networks.",
            "Ordered Crossover (OX) intrinsically guarantees permutation validity without producing invalid duplicate cities.",
            "Easily customizable to incorporate complex real-world constraints such as time windows (VRPTW) and vehicle capacities."
        ]
    elif key == "ga_knapsack":
        return [
            "Dynamic penalty formulation allows exploration through boundary infeasible regions to uncover superior packing solutions.",
            "Scales efficiently to thousands of knapsack items where classical dynamic programming suffers from pseudo-polynomial memory explosion.",
            "Elitism preservation prevents high-value optimal packing allocations from being destroyed during crossover."
        ]
    elif key == "nsga_ii":
        return [
            "Approximates a complete set of Pareto-optimal non-dominated solutions in a single unified execution run.",
            "Crowding distance calculation provides natural, parameterless diversity preservation along the Pareto front.",
            "Completely removes the need for subjective, arbitrary weighting parameters across conflicting engineering objectives."
        ]
    elif key == "differential_evolution":
        return [
            "Self-referential difference vector mutation dynamically scales with population spread, providing self-adaptive step sizes.",
            "Extremely robust performance on non-linear, multi-modal, non-differentiable continuous optimization problems.",
            "Requires very few control parameters (primarily scale factor F and crossover rate CR) and exhibits strong global convergence."
        ]
    elif key == "island_ga":
        return [
            "Coarse-grained sub-population isolation preserves genetic diversity and strongly prevents premature convergence.",
            "Embarrassingly parallelizable across distributed cluster nodes, GPUs, and multi-core CPU architectures.",
            "Super-linear speedup characteristics observed due to localized exploitation coupled with periodic migration."
        ]
    elif key == "adaptive_ga":
        return [
            "Automatically accelerates exploration in stagnation phases while providing fine-grained exploitation near optimal peaks.",
            "Eliminates trial-and-error manual tuning of crossover and mutation hyperparameters.",
            "Preserves elite candidate chromosomes with minimal disruption while mutating low-performing individuals aggressively."
        ]
    else:
        return [
            "Robust global search capability across complex, non-differentiable multimodal landscapes.",
            "Maintains population diversity to avoid trapping in local optima through mutation mechanics.",
            "Applicable to black-box optimization problems where derivative gradients are unavailable."
        ]

def get_ga_disadvantages(algorithm_name: str) -> List[str]:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return [
            "Stochastic heuristic nature means it does not strictly guarantee the exact mathematical global shortest tour.",
            "Convergence slows down significantly on very dense graphs (N > 500 cities) without 2-opt/3-opt hybrid local search memetics."
        ]
    elif key == "ga_knapsack":
        return [
            "Sensitive to penalty multiplier tuning; overly strict penalties eliminate valid search spaces while loose penalties yield infeasible solutions.",
            "Approximate solution quality compared to exact Branch and Bound solvers for small to medium problem instances."
        ]
    elif key == "nsga_ii":
        return [
            "Fast non-dominated sorting scales with O(M * N^2), causing performance degradation for many-objective problems (M > 4).",
            "High computational cost when objective function evaluations involve heavy numerical simulations."
        ]
    elif key == "differential_evolution":
        return [
            "Unsuited for discrete or permutation-based combinatorial problems without special continuous-to-discrete mappings.",
            "Can experience stagnation if population diversity collapses before finding the global basin of attraction."
        ]
    elif key == "island_ga":
        return [
            "Requires hyperparameter tuning for migration topology, migration interval, and migration selection criteria.",
            "Inter-node communication latency in distributed clusters can introduce synchronization bottlenecks."
        ]
    elif key == "adaptive_ga":
        return [
            "Higher computational overhead per generation due to real-time computation of population fitness metrics and dynamic rates.",
            "Adaptive formulation parameters (k1, k2, k3, k4) still require initial empirical bounds."
        ]
    else:
        return [
            "No theoretical guarantee of locating the exact global mathematical optimum within finite generations.",
            "High computational complexity for large population sizes and slow fitness evaluation functions."
        ]

def get_ga_interview_questions(algorithm_name: str) -> List[str]:
    key = get_matched_ga_key(algorithm_name)
    if key == "ga_tsp":
        return [
            "Why does standard 1-point or 2-point crossover produce invalid offspring for TSP, and how does Ordered Crossover (OX) solve this?",
            "What is the difference between Swap Mutation, Inversion Mutation, and Scramble Mutation in permutation GAs?",
            "How can Genetic Algorithms be hybridized with Local Search (Memetic Algorithms like 2-opt) to accelerate TSP convergence?"
        ]
    elif key == "ga_knapsack":
        return [
            "How do penalty functions versus repair mechanisms compare when handling capacity constraints in 0/1 Knapsack GAs?",
            "When would you prefer a Genetic Algorithm over Dynamic Programming or Branch & Bound for the Knapsack problem?",
            "How does elitism prevent the loss of optimal feasible packing subsets during evolutionary selection?"
        ]
    elif key == "nsga_ii":
        return [
            "Explain the concept of Pareto dominance and why scalarized weighted-sum approaches often fail on non-convex Pareto fronts.",
            "How does NSGA-II achieve O(M * N^2) non-dominated sorting complexity compared to naive O(M * N^3) sorting?",
            "What is Crowding Distance, how is it calculated, and why does it eliminate the fitness sharing niche parameter sigma_share?"
        ]
    elif key == "differential_evolution":
        return [
            "How does mutation in Differential Evolution (DE) fundamentally differ from mutation in classical Genetic Algorithms?",
            "Explain the role of the scale factor F and crossover rate CR in DE/rand/1/bin.",
            "Why is Differential Evolution often significantly more effective than standard GAs for continuous numerical optimization?"
        ]
    elif key == "island_ga":
        return [
            "How does the Island Model topology (Ring vs Torus vs Fully Connected) impact genetic diversity and convergence speed?",
            "What is the difference between synchronous and asynchronous migration in distributed parallel evolutionary algorithms?",
            "Why does the Island Model frequently achieve super-linear speedup in real-world benchmark tests?"
        ]
    elif key == "adaptive_ga":
        return [
            "What problem with fixed crossover and mutation rates does the Srinivas-Patnaik Adaptive Genetic Algorithm address?",
            "Why should chromosomes with higher fitness receive lower crossover and mutation rates than below-average chromosomes?",
            "How do self-adaptive GAs (encoding Pc/Pm directly on the chromosome) compare to rule-based adaptive GAs?"
        ]
    else:
        return [
            "Explain Holland's Schema Theorem and the Building Block Hypothesis in Genetic Algorithms.",
            "Compare Roulette Wheel Selection, Tournament Selection, and Rank Selection in terms of selection pressure and genetic drift.",
            "How do you balance exploration (global search via mutation) versus exploitation (local refinement via selection) in GAs?"
        ]
