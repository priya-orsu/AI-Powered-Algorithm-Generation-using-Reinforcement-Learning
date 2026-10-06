"""
Algorithm Technical Interview Q&A Service
Provides comprehensive technical interview questions, detailed model answers,
evaluation criteria, and dynamic question-answering capabilities for computer science algorithms.
"""

import re
from typing import Dict, Any, List, Optional

# Curated High-Yield Interview Q&A for Popular Algorithms
CURATED_INTERVIEW_QA: Dict[str, List[Dict[str, Any]]] = {
    "dijkstra": [
        {
            "id": 1,
            "question": "Why does Dijkstra's algorithm fail on graphs with negative edge weights, and which algorithm should be used instead?",
            "difficulty": "Medium",
            "topic": "Algorithmic Invariants & Edge Cases",
            "answer": "Dijkstra relies on a strict greedy invariant: once a vertex is extracted from the min-heap, its shortest distance from the source is permanently finalized and cannot be decreased further. Negative edge weights violate this assumption because reaching an already-visited vertex through a future edge with a negative weight could yield a shorter path, causing Dijkstra to produce incorrect distances or cycle indefinitely.\n\nFor graphs with negative edge weights, the Bellman-Ford algorithm (or SPFA) must be used. Bellman-Ford relaxes all edges V-1 times in O(V * E) time and can explicitly detect negative weight cycles.",
            "key_points": [
                "Greedy choice property fails because distances are not monotonically increasing.",
                "Bellman-Ford handles negative weights in O(V * E) time.",
                "If a negative cycle exists, shortest paths are undefined (-infinity)."
            ]
        },
        {
            "id": 2,
            "question": "How does the time complexity of Dijkstra's algorithm vary across different priority queue data structures?",
            "difficulty": "Medium",
            "topic": "Complexity & Data Structures",
            "answer": "The time complexity of Dijkstra is O(V * T_extract_min + E * T_decrease_key):\n\n1. Unindexed Array: O(V^2 + E) = O(V^2). Optimal for very dense graphs where E is close to V^2.\n2. Binary Min-Heap: O((V + E) log V). Standard industry choice; efficient for sparse graphs (E << V^2).\n3. Fibonacci Heap: O(E + V log V). Amortized O(1) for decrease-key operations, offering theoretical optimality for dense graphs, though binary heaps often perform better in practice due to lower constant factors and cache locality.",
            "key_points": [
                "Array: O(V^2) is best for dense graphs.",
                "Binary Heap: O((V + E) log V) is standard for sparse graphs.",
                "Fibonacci Heap: O(E + V log V) is theoretically optimal but carries high constant factors."
            ]
        },
        {
            "id": 3,
            "question": "How would you modify Dijkstra's algorithm to reconstruct the exact path sequence, not just the total distance?",
            "difficulty": "Core",
            "topic": "Implementation & Path Reconstruction",
            "answer": "To reconstruct the full path, maintain a `parent` (or `predecessor`) array initialized to None. Whenever an edge (u, v) is relaxed because dist[u] + weight < dist[v], update `parent[v] = u` alongside `dist[v] = dist[u] + weight`.\n\nOnce the destination target T is reached, trace backward from T following parent pointers (T -> parent[T] -> parent[parent[T]] -> ... -> Source) and reverse the resulting list. This reconstructs the optimal path in O(L) time where L is the number of edges on the path.",
            "key_points": [
                "Maintain a predecessor array updated during edge relaxation.",
                "Backtrack from destination to source in O(path length) time.",
                "Space overhead is only O(V) for the parent map."
            ]
        }
    ],

    "binary_search": [
        {
            "id": 1,
            "question": "Why is `mid = low + (high - low) // 2` preferred over `mid = (low + high) // 2` in Binary Search?",
            "difficulty": "Core",
            "topic": "Numerical Robustness & Overflow",
            "answer": "In statically typed languages with 32-bit signed integers (C, C++, Java), integer variables have a maximum value of 2^31 - 1 (2,147,483,647). If `low` and `high` are both large (for example, low = 1.5 billion and high = 2.0 billion), their sum `low + high` equals 3.5 billion, which exceeds the 32-bit limit and overflows into a negative number, causing unexpected crashes or array index errors.\n\nUsing `low + (high - low) // 2` is algebraically identical to (low + high) // 2, but subtracts first, guaranteeing that intermediate calculations never exceed `high`.",
            "key_points": [
                "Prevents 32-bit signed integer overflow in languages like C++, Java, and Go.",
                "Algebraically equivalent: low + (high - low) / 2 = (2*low + high - low) / 2 = (low + high) / 2.",
                "Modern Python handles arbitrary-precision integers automatically, but this remains a fundamental software engineering best practice."
            ]
        },
        {
            "id": 2,
            "question": "How do you modify Binary Search to find the first occurrence (lower bound) and last occurrence (upper bound) of a target in an array with duplicates?",
            "difficulty": "Medium",
            "topic": "Boundary Conditions & Duplicates",
            "answer": "When duplicates exist, you must not terminate immediately when `arr[mid] == target`:\n\n1. First Occurrence (Lower Bound): When `arr[mid] == target`, record `result = mid` as a candidate answer, but keep searching left by setting `high = mid - 1` to check if an earlier match exists.\n2. Last Occurrence (Upper Bound): When `arr[mid] == target`, record `result = mid` as a candidate answer, but keep searching right by setting `low = mid + 1` to check if a later match exists.\n\nBoth variants run in O(log N) time and O(1) space.",
            "key_points": [
                "Never stop on exact match; record candidate and continue narrowing search window.",
                "Left boundary: high = mid - 1.",
                "Right boundary: low = mid + 1.",
                "Preserves strict O(log N) complexity without falling back to linear scan."
            ]
        },
        {
            "id": 3,
            "question": "How can Binary Search be applied to a rotated sorted array (e.g., LeetCode #33)?",
            "difficulty": "Medium",
            "topic": "Rotated Arrays & Invariants",
            "answer": "In any circularly rotated sorted array with no duplicates, picking any `mid` index splits the array into two halves, where AT LEAST ONE half is guaranteed to be sorted uniformly:\n\n1. If `arr[low] <= arr[mid]`, the left half is sorted. Check if `target` lies within `[arr[low], arr[mid]]`. If so, search left (`high = mid - 1`); otherwise search right (`low = mid + 1`).\n2. If `arr[low] > arr[mid]`, the right half must be sorted. Check if `target` lies within `[arr[mid], arr[high]]`. If so, search right (`low = mid + 1`); otherwise search left (`high = mid - 1`).\n\nThis maintains the divide-and-conquer invariant, achieving O(log N) runtime.",
            "key_points": [
                "At least one half is always monotonically sorted.",
                "Determine which half is sorted by comparing arr[low] and arr[mid].",
                "Check if target is within the sorted range to decide which branch to prune."
            ]
        }
    ],

    "merge_sort": [
        {
            "id": 1,
            "question": "Why is Merge Sort preferred over Quick Sort for sorting singly linked lists?",
            "difficulty": "Medium",
            "topic": "Data Structure Adaptation",
            "answer": "Merge Sort is ideal for linked lists for two primary reasons:\n1. O(1) Auxiliary Space: Unlike arrays where merging requires an O(N) temporary buffer, merging two sorted linked lists can be done entirely in-place by adjusting `.next` pointers, requiring zero extra memory allocations.\n2. Sequential Access: Quick Sort requires random access O(1) indexing to efficiently partition arrays (swapping elements across arbitrary indices). In singly linked lists, indexed access takes O(N), making Quick Sort partition inefficient. Merge Sort only requires sequential access and splits lists in O(N) using slow and fast pointers.",
            "key_points": [
                "Linked list Merge Sort needs O(1) auxiliary memory via pointer rewiring.",
                "Quick Sort suffers on linked lists because random indexed access is O(N).",
                "Slow/fast pointer technique divides linked lists in linear time."
            ]
        },
        {
            "id": 2,
            "question": "How can Merge Sort be modified to count the number of inversions in an array in O(N log N) time?",
            "difficulty": "Hard",
            "topic": "Divide and Conquer Adaptation",
            "answer": "An inversion is a pair (i, j) such that i < j and arr[i] > arr[j]. During the standard Merge Sort merge phase of two sorted subarrays `left` and `right`:\n\nWhen comparing `left[i]` with `right[j]`, if `right[j] < left[i]`, then `right[j]` is smaller than EVERY remaining element in `left` from index `i` to `len(left)-1` because `left` is already sorted. Therefore, we immediately add `len(left) - i` to our inversion counter.\n\nThis counts all cross-boundary inversions in O(N log N) total time, compared to O(N^2) for brute force.",
            "key_points": [
                "Inversions are counted directly during the merge step.",
                "If right[j] < left[i], then right[j] is smaller than all (len(left) - i) remaining elements.",
                "Total runtime is O(N log N) with O(N) space."
            ]
        },
        {
            "id": 3,
            "question": "What does stability mean in sorting algorithms, and is Merge Sort stable?",
            "difficulty": "Core",
            "topic": "Algorithm Stability",
            "answer": "A sorting algorithm is stable if elements with equal keys appear in the output in the same relative order as in the original input. For example, if sorting employees first by Department and then by Salary, a stable sort preserves the department ordering for equal salaries.\n\nMerge Sort is stable because during the merge step, when `left[i] == right[j]`, we always pick the element from the left subarray (`left[i]`) first, preserving its original preceding position.",
            "key_points": [
                "Stability preserves original order of duplicate keys.",
                "Merge Sort ensures stability via `if left[i] <= right[j]: take left[i]`.",
                "Quick Sort and Heap Sort are inherently unstable."
            ]
        }
    ],

    "quick_sort": [
        {
            "id": 1,
            "question": "What causes Quick Sort to degrade to its O(N^2) worst case, and how do production implementations avoid it?",
            "difficulty": "Medium",
            "topic": "Worst-Case Mitigation",
            "answer": "Quick Sort degrades to O(N^2) when the chosen pivot consistently partitions the array into maximally unbalanced partitions of size 0 and N-1 (e.g. picking the first or last element of an already sorted or reverse-sorted array).\n\nProduction implementations (like std::sort or Introsort) prevent this using:\n1. Randomized Pivot: Randomly select the pivot element, making the probability of worst-case adversarial input negligible.\n2. Median-of-Three: Choose the median of the first, middle, and last elements.\n3. Introsort (Hybrid Quick Sort): Starts with Quick Sort, monitors recursion depth, and switches to Heap Sort (guaranteed O(N log N)) if recursion depth exceeds 2 * floor(log2 N).",
            "key_points": [
                "Unbalanced splits (0 vs N-1) cause O(N^2) quadratic time.",
                "Randomized pivot and Median-of-Three ensure balanced partitions.",
                "Introsort safeguards with Heap Sort fallback if recursion depth exceeds threshold."
            ]
        },
        {
            "id": 2,
            "question": "How does 3-Way Partitioning (Dutch National Flag) optimize Quick Sort for arrays with many duplicate elements?",
            "difficulty": "Medium",
            "topic": "Duplicate Handling & Partitioning",
            "answer": "Standard 2-way partitioning (Lomuto or Hoare) repeatedly swaps duplicate elements or puts all duplicates into one subproblem, degrading to O(N^2) when an array contains many identical values.\n\n3-Way Partitioning divides the array into three segments: elements smaller than pivot (`< P`), elements equal to pivot (`== P`), and elements greater than pivot (`> P`). After partitioning, all elements equal to the pivot are already in their final sorted positions, allowing Quick Sort to only recurse on the `< P` and `> P` subproblems. For an array of all identical values, this runs in strict O(N) linear time.",
            "key_points": [
                "Partitions into `< P`, `== P`, and `> P` regions.",
                "Elements equal to pivot are finalized in one pass.",
                "Runs in O(N) time on arrays with constant distinct values."
            ]
        }
    ],

    "manacher": [
        {
            "id": 1,
            "question": "How does Manacher's algorithm unify odd-length and even-length palindrome detection into a single pass?",
            "difficulty": "Medium",
            "topic": "String Transformation & Unification",
            "answer": "Even-length palindromes (like `abba`) have their symmetry center between characters, whereas odd-length palindromes (like `aba`) have their center on a character.\n\nManacher's algorithm eliminates this distinction by inserting a unique delimiter character (such as `#`) between every character and at both ends of the string. For example, `'abba'` becomes `'^#a#b#b#a#$'`. In this transformed string, EVERY palindrome has an odd length, and its center is always a single character or delimiter. The length of the original palindrome is simply the radius `P[i]` in the transformed string.",
            "key_points": [
                "Delimiters (`#`) map both even and odd palindromes to odd-length representations.",
                "Original palindrome length directly equals transformed palindrome radius P[i].",
                "Boundary sentinels (`^` and `$`) prevent out-of-bounds array checks."
            ]
        },
        {
            "id": 2,
            "question": "Explain the palindrome mirror property in Manacher's algorithm and why it runs in strict O(N) time.",
            "difficulty": "Hard",
            "topic": "Symmetry Optimization & Amortized Analysis",
            "answer": "Suppose the longest palindrome centered at `C` extends to right boundary `R`. For any index `i < R`, its mirror index across center `C` is `i' = 2*C - i`.\n\nBecause the string is symmetric around `C`, the palindrome radius at `i` is at least `min(R - i, P[i'])`. We only need to perform character expansions if the palindrome at `i` extends beyond `R`.\n\nWhenever a character expansion succeeds, `R` increases. Since `R` starts at 0 and can only advance up to the end of the string (length 2N+3) without ever decreasing, the total number of character comparisons is bounded by O(N), guaranteeing linear execution time.",
            "key_points": [
                "Mirror index: i' = 2*C - i.",
                "Initial radius reuse: P[i] = min(R - i, P[i']).",
                "Character comparisons strictly increment R, bounding total work to O(N)."
            ]
        }
    ],

    "simplex": [
        {
            "id": 1,
            "question": "Why is the Simplex algorithm guaranteed to find the global optimum for linear programming problems?",
            "difficulty": "Medium",
            "topic": "Convex Optimization Theory",
            "answer": "Linear programming problems have two properties that guarantee global optimality:\n1. The set of all feasible solutions forms a convex polytope (bounded by linear inequalities).\n2. The objective function is linear, meaning it is both concave and convex.\n\nBy the Fundamental Theorem of Linear Programming, the optimal value is always attained at one of the extreme points (vertices) of the feasible polytope. The Simplex algorithm pivots from one vertex to an adjacent vertex along the edges of the polytope such that the objective value strictly improves (or remains equal). Since the number of vertices is finite and the region is convex with no local sub-optima, reaching a vertex where no neighboring edge improves the objective guarantees the global optimum.",
            "key_points": [
                "Feasible region is a convex polytope.",
                "Linear objective functions achieve extremes at polytope vertices.",
                "Pivots monotonically improve the objective across adjacent vertices."
            ]
        },
        {
            "id": 2,
            "question": "What is 'degeneracy' in Simplex and how is cycling prevented?",
            "difficulty": "Hard",
            "topic": "Degeneracy & Cycling Prevention",
            "answer": "Degeneracy occurs when a basic feasible solution has one or more basic variables equal to zero. Geometrically, this means more hyperplanes intersect at a vertex than necessary. Pivoting at a degenerate vertex can yield a step size of zero, causing the objective function value to stall.\n\nIf degenerate pivots cycle back to a previously visited basis, the algorithm enters an infinite loop called cycling. Cycling is mathematically prevented using Bland's Rule (smallest subscript rule), which always chooses the entering and leaving variables with the lowest indices among eligible candidates, guaranteeing termination.",
            "key_points": [
                "Degeneracy: Basic variable value is 0, causing zero objective increase.",
                "Cycling: An infinite loop of basis transitions with no objective change.",
                "Bland's Rule: Lowest index selection provably prevents cycling."
            ]
        }
    ],

    "tarjan": [
        {
            "id": 1,
            "question": "What is the distinction between `disc[u]` and `low[u]` in Tarjan's Bridge-Finding algorithm?",
            "difficulty": "Hard",
            "topic": "DFS Low-Link Graph Decomposition",
            "answer": "`disc[u]` is the discovery timestamp (depth counter) indicating when node `u` was first visited in the DFS traversal tree.\n\n`low[u]` is the lowest `disc` timestamp reachable from `u` through its DFS subtree and at most one back-edge.\n\nIf edge (u, v) is a tree edge and `low[v] > disc[u]`, it means the subtree rooted at `v` has no back-edge to `u` or any ancestor of `u`. Therefore, cutting edge (u, v) disconnects `v` and its subtree from the rest of the graph, proving that (u, v) is a critical bridge!",
            "key_points": [
                "disc[u]: Arrival order in DFS.",
                "low[u]: Earliest ancestor reachable via subtree back-edges.",
                "Bridge condition: low[v] > disc[u].",
                "Articulation point condition: low[v] >= disc[u] (for non-root)."
            ]
        }
    ],

    "0/1_knapsack": [
        {
            "id": 1,
            "question": "How can the space complexity of 0/1 Knapsack be optimized from O(N * W) to O(W), and why must the inner loop iterate in reverse?",
            "difficulty": "Medium",
            "topic": "Space Optimization & State Dependencies",
            "answer": "In the standard 2D recurrence `dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt[i]] + val[i])`, computing row `i` depends exclusively on the previous row `i-1`.\n\nWe can compress this into a single 1D array `dp[w]`. However, the capacity loop MUST iterate in reverse from `W` down to `wt[i]`. This ensures that when computing `dp[w - wt[i]]`, the value still represents the state from the previous item (i-1). If we iterated forward, `dp[w - wt[i]]` would have already been updated with item `i`, allowing item `i` to be selected multiple times, which solves the Unbounded Knapsack problem instead of 0/1 Knapsack.",
            "key_points": [
                "Compresses 2D table into a 1D buffer of size W+1.",
                "Iterating backward prevents using the same item multiple times.",
                "Forward iteration transforms the problem into Unbounded Knapsack."
            ]
        },
        {
            "id": 2,
            "question": "What are the two necessary properties required for a problem to be solvable via Dynamic Programming?",
            "difficulty": "Core",
            "topic": "Dynamic Programming Fundamentals",
            "answer": "A problem requires two fundamental structural characteristics to be solved with DP:\n\n1. Optimal Substructure: The optimal solution to the overall problem can be formulated from optimal solutions to its subproblems (e.g. the shortest path from A to C via B contains the shortest path from A to B).\n\n2. Overlapping Subproblems: A recursive formulation encounters the same subproblems repeatedly rather than generating distinct new ones. DP caches (memoizes) these shared sub-solutions in a lookup table to avoid redundant exponential recalculation.",
            "key_points": [
                "Optimal Substructure: Global optimum built from local sub-optima.",
                "Overlapping Subproblems: Re-evaluating the same states multiple times.",
                "Divide & Conquer handles non-overlapping subproblems (e.g. Merge Sort)."
            ]
        }
    ],

    "kadane": [
        {
            "id": 1,
            "question": "How does Kadane's algorithm find the maximum subarray sum in O(N) time and O(1) space, and how do you handle arrays with all negative numbers?",
            "difficulty": "Core",
            "topic": "Greedy Reset & Dynamic Programming",
            "answer": "Kadane's algorithm maintains two variables:\n1. `current_max`: The maximum subarray sum ending at the current index `i`.\n2. `global_max`: The maximum subarray sum discovered across the entire array so far.\n\nAt each element `x`, update `current_max = max(x, current_max + x)`. This makes a greedy choice: either extend the existing subarray by adding `x`, or discard the past and start a fresh subarray starting at `x`.\n\nTo handle arrays where all numbers are negative, initialize `current_max = arr[0]` and `global_max = arr[0]` (instead of 0). This correctly returns the single largest (least negative) element rather than 0.",
            "key_points": [
                "State recurrence: current_max = max(x, current_max + x).",
                "O(N) time complexity in a single linear pass with O(1) extra space.",
                "Initialize with arr[0] to correctly handle all-negative arrays."
            ]
        }
    ],

    "breadth_first_search": [
        {
            "id": 1,
            "question": "Why does BFS guarantee the shortest path on unweighted graphs, and why does it fail on weighted graphs?",
            "difficulty": "Core",
            "topic": "Shortest Path Invariants",
            "answer": "BFS uses a First-In-First-Out (FIFO) queue to explore vertices in strictly non-decreasing order of edge hop count (distance 0, distance 1, distance 2, ...). Therefore, the first time target T is popped from the queue, it has been reached via the path with the minimum number of edges.\n\nOn weighted graphs, a path with FEWER edges can have a HIGHER total weight than an alternate path with MORE edges (e.g., 1 edge of cost 100 vs. 3 edges of cost 1+1+1 = 3). Because BFS does not consider edge costs, it would prematurely finalize the suboptimal 1-edge path. Dijkstra's algorithm solves this by prioritizing path weights using a min-heap instead of FIFO ordering.",
            "key_points": [
                "BFS explores strictly by hop count, optimal when all edge weights are equal.",
                "Fails on weighted graphs because fewer hops != lower total cost.",
                "Dijkstra replaces FIFO queue with Priority Queue to handle weights."
            ]
        }
    ]
}


def normalize_token(text: str) -> str:
    """Strip all non-alphanumeric characters for clean key matching."""
    return re.sub(r'[^a-z0-9]', '', (text or "").lower())


def get_algorithm_interview_qa(
    algorithm_name: str,
    category: str = "",
    problem_statement: str = "",
    time_complexity: str = "O(N log N)",
    space_complexity: str = "O(N)"
) -> List[Dict[str, Any]]:
    """
    Returns high-yield, structured technical interview questions and comprehensive model answers.
    """
    clean_name = (algorithm_name or "").lower().strip()
    norm_name = normalize_token(clean_name)

    # 1. Check Curated High-Yield Interview Database
    for key, qas in CURATED_INTERVIEW_QA.items():
        norm_key = normalize_token(key)
        if norm_key and (norm_key in norm_name or norm_name in norm_key):
            return qas

    # Acronym & special alias lookups
    if "astar" in norm_name or "asearch" in norm_name:
        return [
            {
                "id": 1,
                "question": "What is an 'admissible' heuristic in A* Search, and what happens if a heuristic is inadmissible?",
                "difficulty": "Medium",
                "topic": "Heuristic Admissibility & Optimality",
                "answer": "A heuristic h(n) is admissible if it never overestimates the actual minimal cost to reach the goal from node n: h(n) <= h*(n). When h(n) is admissible (and consistent/monotonic for graph search without re-opening), A* is mathematically guaranteed to return the provably optimal shortest path.\n\nIf h(n) is inadmissible (overestimates costs), A* may prune optimal paths prematurely and return a suboptimal route, trading solution optimality for faster search speeds.",
                "key_points": [
                    "Admissible heuristic: h(n) <= h*(n) (never overestimates).",
                    "Guarantees optimal shortest path when combined with consistency.",
                    "Inadmissible heuristics find solutions faster but forfeit optimality."
                ]
            },
            {
                "id": 2,
                "question": "How does A* Search balance exploration versus exploitation through its f(n) evaluation function?",
                "difficulty": "Core",
                "topic": "Cost Function Architecture",
                "answer": "A* evaluates each node using f(n) = g(n) + h(n), where:\n- g(n): The exact cost accumulated from the start node to current node n (exploitation / past knowledge).\n- h(n): The estimated cost from node n to the destination goal (exploration / future heuristic).\n\nIf h(n) = 0 everywhere, A* degenerates into standard Dijkstra's algorithm. If g(n) is ignored, A* becomes Greedy Best-First Search.",
                "key_points": [
                    "f(n) = g(n) + h(n) balances path history with goal distance.",
                    "h(n) = 0 reduces A* to Dijkstra's algorithm.",
                    "g(n) = 0 turns A* into Greedy Best-First Search."
                ]
            }
        ]

    # 2. Dynamic Domain-Specific Interview Q&A Generator
    cat_lower = (category or "").lower()

    if "sort" in cat_lower or "sort" in clean_name:
        return [
            {
                "id": 1,
                "question": f"What are the best-case, average-case, and worst-case time complexities of {algorithm_name}, and what input causes the worst case?",
                "difficulty": "Core",
                "topic": "Time Complexity & Edge Inputs",
                "answer": f"{algorithm_name} exhibits characteristic complexity trade-offs based on the input arrangement. Under favorable distributions where inputs are already near-sorted or partitioned evenly, operations complete within optimal bounds. The worst-case degradation occurs on adversarial inputs (such as reverse-sorted collections or high duplicate densities) when partitioning or comparisons fail to halve the problem space.",
                "key_points": [
                    f"Analyze worst-case scenarios and input ordering triggers for {algorithm_name}.",
                    "Contrast comparison-based lower bound Omega(N log N) against non-comparison options.",
                    "Verify stability and auxiliary memory requirements."
                ]
            },
            {
                "id": 2,
                "question": f"How does the auxiliary space complexity of {algorithm_name} impact its suitability for memory-constrained embedded systems?",
                "difficulty": "Medium",
                "topic": "Space Complexity & Cache Locality",
                "answer": f"In production systems, auxiliary space complexity determines whether sorting can occur in-place or requires external heap allocation. If {algorithm_name} allocates temporary buffers, memory overhead scales with dataset size, risking Out-Of-Memory (OOM) faults on embedded hardware. In-place algorithms with O(1) extra space or minimal recursion stacks offer superior hardware cache locality and lower allocation latency.",
                "key_points": [
                    "In-place sorting avoids dynamic memory allocation overhead.",
                    "Sequential memory access yields superior L1/L2 CPU cache hit rates.",
                    "Recursion stack limits must be evaluated for deep input trees."
                ]
            },
            {
                "id": 3,
                "question": f"Is {algorithm_name} a stable sorting algorithm, and why does stability matter in production pipelines?",
                "difficulty": "Medium",
                "topic": "Sorting Invariants & Data Integrity",
                "answer": f"Stability guarantees that identical keys retain their original relative positions in the output. In multi-stage data processing pipelines (such as sorting records by Date, then by Transaction Amount), an unstable sort would scramble the primary ordering when processing equal keys. Stability is maintained if comparison checks strictly respect the original order when keys are equal.",
                "key_points": [
                    "Stable sorts preserve relative order of equal keys.",
                    "Crucial for multi-column spreadsheet sorting and database queries.",
                    "Can be achieved in unstable algorithms by appending original index ties."
                ]
            }
        ]

    if "graph" in cat_lower or "tree" in cat_lower or "path" in clean_name:
        return [
            {
                "id": 1,
                "question": f"How does {algorithm_name} handle cyclic dependencies and prevent infinite recursion or processing loops?",
                "difficulty": "Core",
                "topic": "Cycle Detection & Visited State Tracking",
                "answer": f"{algorithm_name} prevents infinite traversal loops by maintaining an explicit visited state collection (such as a hash set, boolean array, or tri-state color markers: Unvisited, In-Progress, Visited). Whenever an adjacent edge points to a node currently marked as In-Progress, a directed cycle is detected.",
                "key_points": [
                    "State tracking array / set guarantees each vertex is expanded at most once.",
                    "Tri-state coloring detects back-edges in directed dependency graphs.",
                    "Ensures overall time complexity remains bounded by O(V + E)."
                ]
            },
            {
                "id": 2,
                "question": f"What is the performance trade-off of representing graphs using an Adjacency Matrix versus an Adjacency List for {algorithm_name}?",
                "difficulty": "Medium",
                "topic": "Graph Data Structures",
                "answer": f"An Adjacency Matrix requires O(V^2) space and O(V) time to inspect neighbors of any node, making it inefficient for sparse graphs where E << V^2. An Adjacency List consumes O(V + E) space and allows immediate iteration over only existing neighbors in O(degree(v)) time, which is optimal for the traversal steps of {algorithm_name}.",
                "key_points": [
                    "Adjacency List is optimal for sparse graphs: O(V + E) space.",
                    "Adjacency Matrix offers O(1) edge existence checks but wastes memory for sparse data.",
                    "Traversal complexity is bounded by degree sum 2E in adjacency lists."
                ]
            }
        ]

    # Universal Fallback for ANY CS Algorithm
    return [
        {
            "id": 1,
            "question": f"What are the primary computational bottlenecks of {algorithm_name}, and how would you optimize it for high-throughput production?",
            "difficulty": "Core",
            "topic": "System Optimization & Scalability",
            "answer": f"The primary bottlenecks of {algorithm_name} stem from state evaluations and memory access patterns. To optimize for high-throughput production, consider:\n1. Algorithmic pruning: discard unpromising states early using bounding heuristics.\n2. Memory efficiency: reuse pre-allocated buffers rather than creating short-lived heap objects.\n3. Parallelization: partition independent subproblems across multi-core CPU threads or SIMD vector instructions.",
            "key_points": [
                f"Identify dominant asymptotic factors: {time_complexity} time and {space_complexity} space.",
                "Prune redundant exploration branches early.",
                "Minimize memory allocations through object pooling and buffer reuse."
            ]
        },
        {
            "id": 2,
            "question": f"What critical edge cases and boundary conditions must be validated when deploying {algorithm_name}?",
            "difficulty": "Medium",
            "topic": "Defensive Engineering & Robustness",
            "answer": f"When implementing {algorithm_name}, test coverage must explicitly validate:\n1. Empty or single-element inputs: ensuring immediate valid termination without null-pointer or index exceptions.\n2. Extreme value ranges: preventing arithmetic integer overflow or underflow on massive numbers.\n3. Duplicate or identical inputs: verifying that state transitions do not degenerate into infinite loops or degraded quadratic performance.",
            "key_points": [
                "Empty, single-element, and maximum-capacity boundary testing.",
                "Numerical overflow prevention in index arithmetic and cost calculations.",
                "Degenerate and uniform input distribution validation."
            ]
        },
        {
            "id": 3,
            "question": f"How does {algorithm_name} compare against alternative standard library approaches in terms of maintainability versus raw performance?",
            "difficulty": "Medium",
            "topic": "Architecture & Engineering Trade-offs",
            "answer": f"While custom implementations of {algorithm_name} can achieve specialized domain-specific optimizations (such as custom memory layouts or vectorized operations), standard library implementations are extensively vetted for edge-case safety, concurrency, and hardware branch prediction. For 90% of use cases, standard primitives are preferred; custom implementations should be reserved for hot paths where profiling proves an algorithmic bottleneck.",
            "key_points": [
                "Profile before optimizing: verify if the algorithm resides on the critical execution path.",
                "Standard library functions benefit from decades of compiler intrinsics and assembly optimizations.",
                "Custom implementations trade engineering maintenance for fine-grained hardware control."
            ]
        }
    ]


def answer_custom_interview_question(
    algorithm_name: str,
    question: str,
    category: str = "",
    problem_statement: str = ""
) -> Dict[str, Any]:
    """
    Answers ANY custom interview question submitted by the user about the specified algorithm.
    """
    q_clean = (question or "").strip().lower()
    algo_clean = (algorithm_name or "").strip()

    # If the question matches one of our curated questions, return its exact authoritative answer
    norm_algo = normalize_token(algo_clean)
    for key, qas in CURATED_INTERVIEW_QA.items():
        if normalize_token(key) in norm_algo:
            for item in qas:
                words_q = set(re.findall(r'\w+', q_clean))
                words_item = set(re.findall(r'\w+', item["question"].lower()))
                overlap = len(words_q.intersection(words_item))
                if overlap >= 4 or (len(words_q) > 0 and overlap / len(words_q) > 0.5):
                    return {
                        "algorithm_name": algo_clean,
                        "question": question,
                        "answer": item["answer"],
                        "difficulty": item["difficulty"],
                        "topic": item["topic"],
                        "key_points": item.get("key_points", []),
                        "source": "Curated Expert Knowledge Base"
                    }

    # Dynamic expert AI answering engine based on question intent
    if any(w in q_clean for w in ["time", "complexity", "big o", "runtime", "worst", "best", "average", "scale"]):
        return {
            "algorithm_name": algo_clean,
            "question": question,
            "topic": "Time & Computational Complexity",
            "difficulty": "Core",
            "answer": f"When evaluating the time complexity of {algo_clean}, operations are characterized by how work scales as input size N increases. In the best case, early-exit heuristics or already-structured inputs allow near-instant completion. The average case reflects standard random distributions, while the worst case occurs when adversarial inputs trigger maximum branching or nested loops. In production interviews, always highlight how choice of underlying data structure (such as hash maps vs. binary trees vs. heaps) shifts runtime bounds.",
            "key_points": [
                f"State the asymptotic bounds clearly for {algo_clean}.",
                "Explain the exact input condition that triggers best vs. worst case behavior.",
                "Discuss the constant-factor overhead and CPU branch predictability in real hardware."
            ],
            "source": "Algorithmic Reasoning Engine"
        }

    elif any(w in q_clean for w in ["space", "memory", "in-place", "auxiliary", "cache", "footprint"]):
        return {
            "algorithm_name": algo_clean,
            "question": question,
            "topic": "Space Complexity & Memory Architecture",
            "difficulty": "Medium",
            "answer": f"The auxiliary space footprint of {algo_clean} depends on whether it can operate in-place using pointer manipulation or requires supplementary data structures (such as hash tables, queues, or recursive stack frames). In high-throughput distributed systems, memory allocation latency often exceeds CPU computation time; thus, avoiding memory fragmentation through buffer reuse or contiguous array buffers is a crucial engineering optimization.",
            "key_points": [
                f"Distinguish input storage from auxiliary working memory for {algo_clean}.",
                "Quantify recursion stack depth (e.g. O(log N) vs O(N)) under worst-case inputs.",
                "Demonstrate memory locality and cache friendly data layout."
            ],
            "source": "Algorithmic Reasoning Engine"
        }

    elif any(w in q_clean for w in ["parallel", "thread", "concurrency", "gpu", "multi-core", "distributed"]):
        return {
            "algorithm_name": algo_clean,
            "question": question,
            "topic": "Concurrency & Parallel Computing",
            "difficulty": "Hard",
            "answer": f"Parallelizing {algo_clean} requires identifying independent subproblems with minimal shared mutable state. If state transitions depend sequentially on previous steps (as in dynamic programming recurrence or sequential graph relaxation), fine-grained synchronization locks can create severe contention bottlenecks. Effective parallelization strategies include domain decomposition, batch parallel evaluation, and lock-free read-only snapshot buffers.",
            "key_points": [
                "Decompose data into independent partitions to minimize inter-thread communication.",
                "Avoid mutex contention on hot state variables.",
                "Leverage vectorization (SIMD) or GPU thread blocks for bulk arithmetic operations."
            ],
            "source": "Algorithmic Reasoning Engine"
        }

    elif any(w in q_clean for w in ["edge", "corner", "fail", "null", "empty", "overflow", "negative"]):
        return {
            "algorithm_name": algo_clean,
            "question": question,
            "topic": "Edge Cases & Defensive Design",
            "answer": f"For {algo_clean}, primary failure modes and edge cases include: (1) Empty or null collections, which should return empty results or raise explicit domain exceptions; (2) Single-element inputs where looping bounds must not cause index-out-of-bounds; (3) Numeric extremes where summing or multiplying indices/weights exceeds integer capacity; and (4) Adversarial duplicate or cyclical patterns that might cause infinite loops or degenerate performance.",
            "key_points": [
                "Validate input bounds and nullability at the API entry point.",
                "Guard against integer overflow using safe arithmetic.",
                "Test against extreme distribution shapes (e.g. all equal elements, reverse sorted)."
            ],
            "source": "Algorithmic Reasoning Engine"
        }

    else:
        return {
            "algorithm_name": algo_clean,
            "question": question,
            "topic": "Algorithmic Architecture & Best Practices",
            "difficulty": "Medium",
            "answer": f"In technical interview scenarios regarding '{question}' for {algo_clean}, the interviewer is evaluating your understanding of trade-offs. The key is to start with the fundamental mathematical or structural invariant that {algo_clean} relies upon, explain how changing the constraints impacts correctness and performance, and propose a concrete optimization or architectural mitigation suitable for large-scale production environments.",
            "key_points": [
                f"Ground your answer in the core algorithmic invariant of {algo_clean}.",
                "State trade-offs explicitly (time vs. space vs. engineering maintainability).",
                "Provide a concrete, production-ready implementation recommendation."
            ],
            "source": "Algorithmic Reasoning Engine"
        }
