import sys

with open("app/services/genetic_algorithms_catalog.py", "w", encoding="utf-8") as f:
    f.write('''"""
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
''')

print("Part 1 written")
