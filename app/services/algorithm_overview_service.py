"""
Algorithm Overview & Intuition Service
Provides clear, human-understandable algorithmic explanations, mental models,
paradigms, input/output specifications, and when-to-use / when-to-avoid guidelines.
"""

import re
from typing import Dict, Any, List

# Curated high-precision overview intuitions for prominent CS algorithms
ALGORITHM_INTUITIONS: Dict[str, Dict[str, Any]] = {
    "dijkstra": {
        "intuitive_explanation": "Think of Dijkstra's algorithm like ripples of water expanding outward through a network of pipes at speeds proportional to pipe lengths. By always exploring the closest unvisited junction first using a min-heap, it guarantees that the first time a destination junction is reached, it is via the absolute shortest route possible.",
        "paradigm": "Greedy / Priority Queue Edge Relaxation",
        "key_data_structures": ["Min-Heap / Priority Queue", "Adjacency List", "Distance Hash Map"],
        "input_spec": "Weighted graph G = (V, E) with non-negative edge weights and a designated source vertex S.",
        "output_spec": "Array/Map mapping every reachable vertex to its minimum distance and predecessor path from S.",
        "when_to_use": [
            "Finding the quickest or lowest-cost route from one source node to all other nodes (e.g. GPS maps, router packet forwarding).",
            "Graphs with non-negative edge weights where immediate greedy expansion is provably optimal."
        ],
        "when_not_to_use": [
            "Graphs containing negative edge weights or negative weight cycles — use Bellman-Ford or SPFA instead.",
            "Unweighted graphs where standard Breadth-First Search (BFS) is faster (O(V+E) vs O((V+E) log V))."
        ],
        "key_takeaway": "Greedily relax the closest known node; once popped from the priority queue, its shortest distance is permanently finalized."
    },
    "binary_search": {
        "intuitive_explanation": "Imagine looking up a word in a printed dictionary: you don't read page 1 through 1000. You flip directly to the exact middle, check if your word comes alphabetically before or after, and instantly discard half the remaining book with every single flip.",
        "paradigm": "Divide and Conquer / Interval Halving",
        "key_data_structures": ["Sorted Array / Continuous Monotonic Space", "Left/Right Pointers"],
        "input_spec": "A sorted collection of N elements (or monotonic mathematical function) and a target search key.",
        "output_spec": "The exact index position of the key if found, or insertion boundary / -1 if absent.",
        "when_to_use": [
            "Searching for a value in sorted arrays or contiguous memory buffers in lightning-fast O(log N) steps.",
            "Optimizing parameters over monotonic answer spaces (e.g. 'Binary Search on Answer' for capacity thresholds)."
        ],
        "when_not_to_use": [
            "Unsorted datasets where sorting first takes O(N log N) which exceeds a simple linear scan O(N).",
            "Linked lists where random indexed access O(1) is unavailable (use Skip Lists or BSTs instead)."
        ],
        "key_takeaway": "Every comparison cuts the candidate search space in half, finding needles in billion-item datasets in just 30 comparisons."
    },
    "merge_sort": {
        "intuitive_explanation": "Imagine sorting a large stack of exam papers: you split the stack in half and hand each half to an assistant. Once both smaller stacks are sorted, you simply zip them together by comparing the top papers from each stack one by one.",
        "paradigm": "Divide and Conquer (Recursive Split & Merge)",
        "key_data_structures": ["Temporary Auxiliary Buffers", "Subarray Pointers"],
        "input_spec": "An unordered list or array of N comparable items.",
        "output_spec": "A strictly sorted permutation in non-decreasing order with identical relative ordering of equal keys (Stable).",
        "when_to_use": [
            "When stability (preserving original order of equal items) is mandatory (e.g. sorting by price, then by rating).",
            "External sorting of massive datasets too large to fit in RAM (e.g. hard disk tape merges)."
        ],
        "when_not_to_use": [
            "Embedded systems with severely constrained memory, since standard Merge Sort requires O(N) auxiliary space.",
            "Small in-memory arrays where In-Place Quick Sort or Insertion Sort have lower constant factors."
        ],
        "key_takeaway": "Guaranteed deterministic O(N log N) worst-case time complexity, immune to the adversarial pivot pitfalls of Quick Sort."
    },
    "quick_sort": {
        "intuitive_explanation": "Pick one student as a benchmark 'pivot', and tell everyone shorter to stand on the left and everyone taller to stand on the right. Repeat this process for the left and right groups independently until the entire class is in order.",
        "paradigm": "Divide and Conquer (In-Place Partitioning)",
        "key_data_structures": ["In-Place Array", "Partition Pointers (Lomuto or Hoare)"],
        "input_spec": "An unsorted array of N elements.",
        "output_spec": "In-place sorted array with zero auxiliary memory allocation.",
        "when_to_use": [
            "General-purpose in-memory sorting where cache locality and O(1) space efficiency are paramount.",
            "Finding the K-th smallest/largest element in linear average O(N) time (via Quickselect)."
        ],
        "when_not_to_use": [
            "Mission-critical systems requiring strict worst-case guarantees (poor pivot choices degrade to O(N^2) without median-of-three/intro-sort).",
            "Applications requiring stable sorting (standard Quick Sort swaps non-adjacent elements)."
        ],
        "key_takeaway": "Extremely fast in practice due to exceptional hardware CPU cache hit rates and minimal overhead."
    },
    "0/1_knapsack": {
        "intuitive_explanation": "Imagine packing a hiking backpack with weight limit W: for every piece of gear, you face a binary choice: leave it behind, or pack it and accept its weight while earning its utility. Dynamic programming records the best possible utility for every weight limit from 0 to W so you never redo calculations.",
        "paradigm": "Dynamic Programming (Optimal Substructure & Memoization)",
        "key_data_structures": ["2D DP Array dp[i][w] or Space-Optimized 1D Buffer dp[w]"],
        "input_spec": "Array of N item weights, array of N item values, and maximum capacity W.",
        "output_spec": "Maximum total value achievable without exceeding total weight capacity W.",
        "when_to_use": [
            "Resource allocation, budget expenditure optimization, and cargo loading problems with indivisible discrete items.",
            "Subset sum and equal partition problems in financial planning."
        ],
        "when_not_to_use": [
            "When items can be divided into fractions (use Greedy fractional knapsack sorted by value/weight in O(N log N)).",
            "When weight capacity W is astronomically large (e.g. W = 10^12), as pseudo-polynomial DP memory would explode."
        ],
        "key_takeaway": "Avoids 2^N exponential brute-force by reusing optimal sub-solutions: dp[w] = max(dp[w], dp[w - weight] + value)."
    },
    "manacher": {
        "intuitive_explanation": "Palindromes are mirror symmetric around their centers. If you've already found a large palindrome around center C, any smaller palindrome to the left of C is mirrored on the right side of C! Manacher's algorithm uses this mirror property to skip redundant character checks, finding all palindromic substrings in a single linear pass.",
        "paradigm": "String Symmetry Exploitation & Two Pointers",
        "key_data_structures": ["Radius Array P[i]", "Transformed Delimiter String (#a#b#a#)"],
        "input_spec": "Any character string S of length N.",
        "output_spec": "The longest palindromic substring or an array of palindrome radii for all center positions.",
        "when_to_use": [
            "Finding the longest palindromic substring or counting all palindromic substrings in strict linear O(N) time.",
            "DNA sequence motif discovery and biological palindrome analysis where quadratic O(N^2) checks would stall."
        ],
        "when_not_to_use": [
            "When the string is very short (N < 20), where simple center-expansion is simpler to implement with negligible difference."
        ],
        "key_takeaway": "Eliminates quadratic string matching by reusing pre-computed palindrome radii through center-boundary mirroring."
    },
    "simplex": {
        "intuitive_explanation": "Imagine the set of all feasible business decisions as the vertices and flat faces of a multi-dimensional crystal. Because linear functions always reach their peak at one of the outer corner vertices, the Simplex algorithm simply climbs from one corner to an adjacent higher corner along the edges until no higher neighbor exists.",
        "paradigm": "Polyhedral Geometry & Linear Algebra Pivot Operations",
        "key_data_structures": ["Simplex Tableau Matrix", "Basis Index Set", "Pivot Row/Column Selectors"],
        "input_spec": "Linear objective function coefficients vector c, constraint matrix A, and requirement vector b.",
        "output_spec": "Optimal decision variable vector x* maximizing objective z, or certificate of unboundedness/infeasibility.",
        "when_to_use": [
            "Industrial operations research: oil refinery scheduling, airline crew scheduling, and supply chain logistics.",
            "Solving large systems of linear inequalities with continuous variables."
        ],
        "when_not_to_use": [
            "Non-linear objective functions (use Gradient Descent, Newton-Raphson, or SQP).",
            "Integer-only problems where variables cannot be fractional (use Branch and Bound or Cutting Plane integer solvers)."
        ],
        "key_takeaway": "Navigates adjacent vertices of the feasible region polytope; mathematically guaranteed to locate the global optimum."
    },
    "tarjan": {
        "intuitive_explanation": "A bridge is a single highway whose destruction cuts off two towns. Tarjan's algorithm sends a DFS scout through the road network, numbering each intersection by arrival time. Each node also tracks the oldest intersection its road or detour can loop back to ('low-link'). If a road leads to a town with no backdoor to earlier intersections, that road is a critical bridge!",
        "paradigm": "Depth-First Search Low-Link Graph Decomposition",
        "key_data_structures": ["Discovery Timer Array", "Low-Link Array", "Recursion Call Stack"],
        "input_spec": "Connected or disconnected graph G = (V, E).",
        "output_spec": "List of critical bridge edges, articulation vertices, or partitioned Strongly Connected Components (SCCs).",
        "when_to_use": [
            "Detecting single points of failure in power grids, internet routing backbones, and server cluster topologies.",
            "Decomposing directed dependency graphs into independent cycle components."
        ],
        "when_not_to_use": [
            "Dynamically mutating networks where edges are constantly added and removed (use dynamic bridge-finding or disjoint-set variants)."
        ],
        "key_takeaway": "Achieves complete structural vulnerability mapping in a single O(V + E) linear depth-first pass."
    },
    "hopcroft_karp": {
        "intuitive_explanation": "Imagine matching job applicants to open positions: each applicant is qualified for several jobs. Hopcroft-Karp finds maximum pairings not by matching one applicant at a time, but by running BFS to find multiple disjoint 'augmenting chains' simultaneously and then zipping all of them in a single batch with DFS.",
        "paradigm": "Multi-Phase BFS/DFS Augmenting Path Maximization",
        "key_data_structures": ["Layered Distance Array", "Pairing Map (Pair_U, Pair_V)", "BFS Queue"],
        "input_spec": "Unweighted bipartite graph G = (U, V, E).",
        "output_spec": "The maximum cardinality matching pairing subsets of U with subsets of V without conflicts.",
        "when_to_use": [
            "Matching doctors to residency hospitals, ride-share drivers to passengers, and tasks to specialized workers.",
            "Finding minimum vertex covers and maximum independent sets in bipartite graphs via Konig's theorem."
        ],
        "when_not_to_use": [
            "When edges have variable monetary weights or costs (use Hungarian / Kuhn-Munkres algorithm instead)."
        ],
        "key_takeaway": "Runs in O(E * sqrt(V)) time by finding all shortest augmenting paths in parallel each phase, dramatically outpacing Ford-Fulkerson."
    },
    "cooley_tukey_fft": {
        "intuitive_explanation": "Any complex sound wave is just a combination of simple pure musical tones. The Cooley-Tukey FFT takes a recording of sound over time and rapidly separates it into its pure ingredient musical frequencies by splitting even and odd audio samples recursively, reducing what would be N^2 calculations down to N log N.",
        "paradigm": "Divide and Conquer (Radix-2 Butterfly Operations)",
        "key_data_structures": ["Complex Number Arrays (Real, Imaginary)", "Twiddle Factor Roots of Unity"],
        "input_spec": "A sequence of N time-domain signal samples (where N is typically a power of 2) or polynomial coefficients.",
        "output_spec": "The exact frequency spectrum (amplitudes and phases) or product polynomial coefficients.",
        "when_to_use": [
            "Audio/video signal processing, noise reduction, image filtering, and MRI scanning.",
            "Ultra-fast polynomial multiplication and large integer arithmetic (multiplying million-digit numbers in O(N log N))."
        ],
        "when_not_to_use": [
            "Very small vectors (N < 16) where direct multiplication constant factors are smaller.",
            "Non-periodic, unstructured spatial lookups."
        ],
        "key_takeaway": "Transforms expensive quadratic operations into logarithmic frequency domain multiplications using roots-of-unity symmetry."
    },
    "skip_list": {
        "intuitive_explanation": "Imagine an express subway train that only stops at major stations (every 8th stop), while a local train stops at every single station. To reach station #43, you take the express train to station #40, and then switch to the local train for the last 3 stops! A Skip List creates multiple express layers above a linked list using coin flips, giving O(log N) speeds without complex tree rotations.",
        "paradigm": "Probabilistic Layered Indexing",
        "key_data_structures": ["Multi-Level Forward Pointer Nodes", "Random Level Generator"],
        "input_spec": "Sequential insert, search, and delete commands with numeric or comparable keys.",
        "output_spec": "O(log N) expected time retrieval without rebalancing bottlenecks.",
        "when_to_use": [
            "High-concurrency in-memory databases (e.g. Redis Sorted Sets, LevelDB, RocksDB) because multi-threaded locking is much simpler than rebalancing AVL/Red-Black trees.",
            "Systems needing ordered key iteration alongside fast logarithmic lookups."
        ],
        "when_not_to_use": [
            "Applications demanding strictly deterministic worst-case bounds, as bad coin flips can theoretically degrade to O(N)."
        ],
        "key_takeaway": "Provides the search, insert, and delete speed of a balanced binary tree, but with simpler node structures and superior multi-core concurrency."
    },
    "breadth_first_search": {
        "intuitive_explanation": "Like dropping a pebble in calm water, BFS spreads outward in perfect concentric rings. It visits every immediate neighbor (1 step away), then all secondary neighbors (2 steps away), and so on. This guarantees that the first time it encounters the target, it has found the path with the fewest possible hops.",
        "paradigm": "Queue-Based Layered Graph Traversal",
        "key_data_structures": ["First-In First-Out (FIFO) Queue", "Visited Set / Boolean Array"],
        "input_spec": "Graph G = (V, E) and a designated root start node S.",
        "output_spec": "Shortest path in terms of edge count from S to all reachable vertices, or level-order traversal order.",
        "when_to_use": [
            "Finding the shortest path on unweighted graphs (e.g. degrees of separation on LinkedIn/Facebook).",
            "Broadcasting messages through peer-to-peer networks and web crawling."
        ],
        "when_not_to_use": [
            "Weighted graphs with varying edge costs (use Dijkstra's algorithm instead).",
            "Deep graph traversals where memory is limited, as the FIFO queue can store O(V) nodes in wide graphs."
        ],
        "key_takeaway": "Explores level-by-level using a FIFO queue; guaranteed to find the minimum number of hops in unweighted graphs."
    },
    "depth_first_search": {
        "intuitive_explanation": "Think of exploring a maze with a ball of string: walk down one corridor as far as it goes until you hit a dead end. Then retrace your steps back to the last fork in the path and explore the next uncharted hallway.",
        "paradigm": "Recursive Backtracking & Exhaustive Search",
        "key_data_structures": ["Call Stack / Explicit LIFO Stack", "Visited State Tracker"],
        "input_spec": "Graph or tree structure G = (V, E) and start vertex.",
        "output_spec": "Traversed vertex ordering, cycle detection status, or topological order.",
        "when_to_use": [
            "Cycle detection in networks and topological ordering of task dependencies.",
            "Solving constraint satisfaction puzzles (Sudoku, N-Queens, maze escapes) via backtracking."
        ],
        "when_not_to_use": [
            "Finding the shortest path in unweighted graphs (DFS may dive down an infinite detour before finding a direct path).",
            "Very deep graphs with millions of levels without tail-call optimization, risking stack overflow."
        ],
        "key_takeaway": "Plunges as deep as possible before backtracking; ideal for exhaustive exploration, connectivity checks, and topological sorting."
    },
    "bellman_ford": {
        "intuitive_explanation": "If a shortest path has no cycles, it can contain at most V-1 edges. Bellman-Ford simply relaxes every single edge in the entire graph V-1 times. If an edge can STILL be relaxed on the V-th round, you have detected a destructive negative-weight cycle!",
        "paradigm": "Dynamic Programming / Systematic Edge Relaxation",
        "key_data_structures": ["Distance Array dist[V]", "Predecessor Array parent[V]"],
        "input_spec": "Directed graph with arbitrary edge weights (positive or negative) and start source S.",
        "output_spec": "Shortest distances from source to all vertices, or a flag reporting the presence of a negative cycle.",
        "when_to_use": [
            "Distance-vector network routing protocols (e.g. RIP protocol in telecommunications).",
            "Detecting currency arbitrage opportunities in financial forex exchange markets."
        ],
        "when_not_to_use": [
            "Large graphs with strictly non-negative weights where Dijkstra is drastically faster (O((V+E) log V) vs O(V*E))."
        ],
        "key_takeaway": "Relaxes all edges V-1 times; handles negative edge weights safely and exposes negative cost infinite loops."
    },
    "floyd_warshall": {
        "intuitive_explanation": "For every pair of cities (i, j), ask: 'Would my trip be shorter if I took a detour through city k?' By trying every possible intermediate city k from 1 to V, the shortest detour between every possible pair is systematically discovered.",
        "paradigm": "Dynamic Programming (All-Pairs Shortest Path)",
        "key_data_structures": ["2D Adjacency Matrix D[V][V]"],
        "input_spec": "Dense or sparse graph with V vertices and edge weights without negative cycles.",
        "output_spec": "A complete V x V distance matrix giving the minimum distance between every single pair of vertices.",
        "when_to_use": [
            "Dense graphs needing distance lookups between all pairs of nodes (e.g. airline flight route planners).",
            "Transitive closure computation and calculating network graph diameters."
        ],
        "when_not_to_use": [
            "Single-source queries (use Dijkstra O(E log V) instead of O(V^3)).",
            "Graphs with thousands of vertices (V > 1000) where O(V^3) runtime becomes prohibitive."
        ],
        "key_takeaway": "Triply nested loops test every intermediate waypoint: D[i][j] = min(D[i][j], D[i][k] + D[k][j])."
    },
    "kruskal": {
        "intuitive_explanation": "Lay all possible roads on a table and sort them from cheapest to most expensive. Pick the cheapest road and pave it — unless it forms a closed loop with roads you already paved! Repeat until every town is connected.",
        "paradigm": "Greedy Edge Selection with Disjoint-Set Union (DSU)",
        "key_data_structures": ["Sorted Edge List", "Disjoint-Set Union (Union-Find)"],
        "input_spec": "Connected, undirected graph G = (V, E) with edge weights.",
        "output_spec": "A Minimum Spanning Tree (MST) connecting all V vertices with exactly V-1 edges and minimum total weight.",
        "when_to_use": [
            "Designing minimum-cost physical utility networks (electrical grids, water pipelines, cable layout).",
            "Clustering algorithms in machine learning (Single-Linkage Hierarchical Clustering)."
        ],
        "when_not_to_use": [
            "Dense graphs where edge count E approaches V^2 (Prim's algorithm with Fibonacci heap is faster in dense cases)."
        ],
        "key_takeaway": "Greedily picks the smallest available edge that connects two previously disconnected components."
    },
    "prim": {
        "intuitive_explanation": "Start from any single seed town. Look at all roads leading out of your current network to uncharted towns, pick the absolute cheapest one, and expand your network to include that town. Keep expanding the frontier greedily until all towns are absorbed.",
        "paradigm": "Greedy Frontier Expansion via Priority Queue",
        "key_data_structures": ["Min-Heap / Priority Queue", "Visited / In-MST Boolean Array"],
        "input_spec": "Connected, undirected graph G = (V, E) with edge costs.",
        "output_spec": "Minimum Spanning Tree (MST) spanning all V vertices with minimal total cost.",
        "when_to_use": [
            "Dense networks where edges are abundant (E ~ V^2).",
            "Real-time network expansion where the tree grows outward from an existing central server or hub."
        ],
        "when_not_to_use": [
            "Sparse graphs with few edges where Kruskal's algorithm with simple edge sorting is faster and easier to code."
        ],
        "key_takeaway": "Grows a single continuous tree outward by always pulling in the cheapest external border edge."
    },
    "a_star": {
        # also matches a_search
    },
    "a_search": {
        "intuitive_explanation": "Dijkstra searches blindly in all directions like an expanding balloon. A* straps a compass to Dijkstra: it adds an educated guess (heuristic h(n)) estimating how far each node is from the final goal, pulling the search directly toward the target like a magnet.",
        "paradigm": "Heuristic Best-First Search (f(n) = g(n) + h(n))",
        "key_data_structures": ["Priority Queue / Min-Heap", "Open and Closed Sets", "Cost Map g(n)"],
        "input_spec": "Graph or grid with edge costs, start node, goal node, and an admissible heuristic function h(n).",
        "output_spec": "The exact optimal path from start to goal in minimal visited nodes.",
        "when_to_use": [
            "Video game NPC navigation, autonomous vehicle trajectory planning, and robotic motion mapping.",
            "Pathfinding on 2D/3D grids with Euclidean or Manhattan distance heuristics."
        ],
        "when_not_to_use": [
            "When no admissible heuristic can be formulated (degenerates to standard Dijkstra).",
            "Multi-target searches where all destination nodes must be reached at once."
        ],
        "key_takeaway": "Prunes search space dramatically by balancing known cost g(n) with estimated distance to target h(n)."
    },
    "dummy_marker": {
        "intuitive_explanation": "Dijkstra searches blindly in all directions like an expanding balloon. A* straps a compass to Dijkstra: it adds an educated guess (heuristic h(n)) estimating how far each node is from the final goal, pulling the search directly toward the target like a magnet.",
        "paradigm": "Heuristic Best-First Search (f(n) = g(n) + h(n))",
        "key_data_structures": ["Priority Queue / Min-Heap", "Open and Closed Sets", "Cost Map g(n)"],
        "input_spec": "Graph or grid with edge costs, start node, goal node, and an admissible heuristic function h(n).",
        "output_spec": "The exact optimal path from start to goal in minimal visited nodes.",
        "when_to_use": [
            "Video game NPC navigation, autonomous vehicle trajectory planning, and robotic motion mapping.",
            "Pathfinding on 2D/3D grids with Euclidean or Manhattan distance heuristics."
        ],
        "when_not_to_use": [
            "When no admissible heuristic can be formulated (degenerates to standard Dijkstra).",
            "Multi-target searches where all destination nodes must be reached at once."
        ],
        "key_takeaway": "Prunes search space dramatically by balancing known cost g(n) with estimated distance to target h(n)."
    },
    "kmp": {
        "intuitive_explanation": "When searching for a word in a book and a letter mismatches, don't restart reading from the very next character! KMP inspects the characters already matched and slides the search pattern forward to the longest prefix that is also a suffix, never rereading a single text character.",
        "paradigm": "Deterministic Finite Automaton / Prefix-Suffix Preprocessing",
        "key_data_structures": ["Prefix Function / LPS (Longest Proper Prefix which is also Suffix) Array"],
        "input_spec": "Text document T of length N and pattern string P of length M.",
        "output_spec": "All start index positions where pattern P occurs within text T in deterministic O(N + M) time.",
        "when_to_use": [
            "Real-time streaming text inspection and intrusion detection systems where rewind buffers are impossible.",
            "Bioinformatics string pattern analysis and fast keyword matching in compilers."
        ],
        "when_not_to_use": [
            "Tiny search patterns (M < 4) where naive search overhead is lower.",
            "Multi-pattern searches where Aho-Corasick or Trie-based matching handles thousands of words at once."
        ],
        "key_takeaway": "Never rewinds the text pointer; the LPS table tells the pattern exactly how far to slide forward upon mismatch."
    },
    "kadane": {
        "intuitive_explanation": "Imagine walking along a street picking up cash or paying fines. At every step, ask: 'Is it better to add this block's cash/fine to my ongoing streak, or cut my losses, throw away the past, and start a fresh streak right here?' Keep track of the best streak seen so far.",
        "paradigm": "Dynamic Programming (Linear Scan with Greedy Reset)",
        "key_data_structures": ["Two scalar variables: current_max, global_max"],
        "input_spec": "Array of N numbers containing both positive and negative values.",
        "output_spec": "The maximum contiguous subarray sum achievable in a single O(N) pass with O(1) memory.",
        "when_to_use": [
            "Financial market analysis to find maximum profit intervals in stock volatility curves.",
            "Computer vision brightness window detection and genomic GC-content peak detection."
        ],
        "when_not_to_use": [
            "Non-contiguous subsequence problems (use 0/1 Knapsack or Longest Increasing Subsequence instead)."
        ],
        "key_takeaway": "Decides in O(1) space whether to extend the current running subarray or start over at the current element."
    }
}


def normalize_token(text: str) -> str:
    """Strip all non-alphanumeric characters for clean key matching."""
    return re.sub(r'[^a-z0-9]', '', (text or "").lower())


def generate_algorithm_overview(
    algorithm_name: str,
    category: str = "",
    description: str = "",
    problem_statement: str = ""
) -> Dict[str, Any]:
    """
    Synthesizes an efficient, clear, human-understandable overview breakdown for ANY CS algorithm.
    """
    clean_name = (algorithm_name or "").lower().strip()
    clean_cat = (category or "").lower().strip()
    norm_name = normalize_token(clean_name)

    # 1. Check curated database for exact/canonical matches using normalized tokens
    for key, data in ALGORITHM_INTUITIONS.items():
        norm_key = normalize_token(key)
        if norm_key and (norm_key in norm_name or norm_name in norm_key):
            return data
    
    # Check special acronyms / short patterns
    if "astar" in norm_name or "asearch" in norm_name:
        return ALGORITHM_INTUITIONS.get("a_star") or ALGORITHM_INTUITIONS.get("a_search")
    if "bfs" in norm_name:
        return ALGORITHM_INTUITIONS.get("breadth_first_search")
    if "dfs" in norm_name:
        return ALGORITHM_INTUITIONS.get("depth_first_search")

    # 2. Dynamic Domain-Specific Intuition Generator for any other algorithm
    if "sort" in clean_cat or "sort" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} organizes unordered data into ordered sequence. It systematically rearranges elements by comparing candidates and minimizing wasteful passes, ensuring reliable indexing, fast search lookups, and deterministic ordering.",
            "paradigm": "Comparison & Partitioning / Sorting",
            "key_data_structures": ["Sequential Array / Buffer", "Swap Pointers"],
            "input_spec": "Collection of N unsorted elements with defined comparison operators.",
            "output_spec": "The same elements arranged in strict ascending or descending sequence.",
            "when_to_use": [
                "Preparing raw datasets for lightning-fast binary search lookups.",
                "Deduplicating elements and grouping identical items together."
            ],
            "when_not_to_use": [
                "When data is already sorted and only a single item is being inserted (use insertion/binary search instead)."
            ],
            "key_takeaway": "Transforms chaos into order so subsequent search and retrieval operations run in optimal time."
        }

    if "search" in clean_cat or "search" in clean_name or "query" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} systematically queries an information space to pinpoint target elements without examining every possibility. It prunes non-promising candidate paths to retrieve results with minimal latency.",
            "paradigm": "Search Space Pruning & State Retrieval",
            "key_data_structures": ["Lookup Table / Index", "Candidate Boundary Pointers"],
            "input_spec": "A dataset or state space of items and a query predicate or target key.",
            "output_spec": "The matching target item, exact index location, or confirmation of absence.",
            "when_to_use": [
                "Locating specific records in large datasets with high performance constraints.",
                "Searching configuration parameter spaces for valid operating points."
            ],
            "when_not_to_use": [
                "Small arrays (N < 10) where a direct linear scan has zero initialization overhead."
            ],
            "key_takeaway": "Quickly narrows down search candidate spaces to deliver answers in logarithmic or sub-linear time."
        }

    if "graph" in clean_cat or "path" in clean_name or "network" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} navigates interconnected networks of nodes and relationships. It systematically evaluates paths, connects optimal communication routes, or eliminates redundancies without getting trapped in cycles.",
            "paradigm": "Graph Traversal & Structural Optimization",
            "key_data_structures": ["Adjacency List / Matrix", "Visited State Tracker", "Priority Queue / Queue"],
            "input_spec": "Graph topology represented as vertices V and connecting edges E with associated weights or capacities.",
            "output_spec": "Optimal routes, connected component clusters, or topological sequence order.",
            "when_to_use": [
                "Network packet routing, supply chain distribution, and map pathfinding.",
                "Analyzing dependency hierarchies and cycle prevention."
            ],
            "when_not_to_use": [
                "Flat tabular datasets with no inter-entity relationships (use standard array/hash lookups)."
            ],
            "key_takeaway": "Explores complex relational spaces efficiently by pruning redundant paths and memorizing visited junctions."
        }

    if "dynamic" in clean_cat or "dp" in clean_name or "knapsack" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} breaks down a massive, intimidating problem into simple, overlapping sub-decisions. By calculating the solution to each small sub-decision once and storing it in a table, it avoids wasteful re-calculations and achieves optimal solutions in polynomial time.",
            "paradigm": "Dynamic Programming (State Transitions & Memoization)",
            "key_data_structures": ["State Matrix / Table", "Memoization Cache Map"],
            "input_spec": "Multi-stage decision parameters, bounds, and transition weights.",
            "output_spec": "The global optimal metric (minimum cost, maximum gain, or optimal sequence choice).",
            "when_to_use": [
                "Optimization problems exhibiting optimal substructure and heavily overlapping sub-problems.",
                "Finding global extremes where greedy local choices fail to yield the best outcome."
            ],
            "when_not_to_use": [
                "Problems with no overlapping sub-problems (use Divide and Conquer).",
                "Scenarios where local greedy choices are already provably optimal."
            ],
            "key_takeaway": "Those who cannot remember the past are condemned to repeat it — dynamic programming saves past answers to guarantee fast global decisions."
        }

    if "string" in clean_cat or "pattern" in clean_name or "text" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} processes character sequences and text streams. It skips redundant character inspections by leveraging pre-computed prefix, suffix, or symmetry properties, finding target patterns in linear time.",
            "paradigm": "String Preprocessing & Deterministic Pattern Scanning",
            "key_data_structures": ["Preprocessing Table / Failure Function", "Character Buffer"],
            "input_spec": "Target text document T of length N and search pattern P of length M.",
            "output_spec": "Start index positions of all matching patterns or structural string features.",
            "when_to_use": [
                "Text editors, DNA genomic motif searching, search engine web indexing, and plagiarism detection."
            ],
            "when_not_to_use": [
                "Searching single characters or very small strings where naive loop scanning is practically instantaneous."
            ],
            "key_takeaway": "Uses mathematical structure within text to fast-forward through characters without backtrack rescanning."
        }

    if "tree" in clean_cat or "tree" in clean_name or "structure" in clean_cat:
        return {
            "intuitive_explanation": f"{algorithm_name} organizes hierarchical data so that items can be inserted, retrieved, or updated in logarithmic time. It maintains balance invariants to prevent performance bottlenecks.",
            "paradigm": "Hierarchical Branching & Balanced Indexing",
            "key_data_structures": ["Tree Nodes with Left/Right or Multi-Way Child Pointers"],
            "input_spec": "Stream of items or records with unique searchable keys.",
            "output_spec": "Dynamically organized hierarchical structure supporting instant search and ordered traversals.",
            "when_to_use": [
                "Database indexing, memory management page tables, and priority job scheduling."
            ],
            "when_not_to_use": [
                "Fixed static collections where simple sorted arrays with binary search offer less pointer memory overhead."
            ],
            "key_takeaway": "Balances data organization dynamically so search depth never degrades to linear time."
        }

    if "optimization" in clean_cat or "linear" in clean_name or "simplex" in clean_name:
        return {
            "intuitive_explanation": f"{algorithm_name} explores multi-dimensional decision boundaries to find the best possible combination of choices that maximize efficiency or profit while respecting real-world constraints.",
            "paradigm": "Mathematical Optimization & Constraint Satisfaction",
            "key_data_structures": ["Constraint Matrix", "Objective Function Vectors", "Decision State Variables"],
            "input_spec": "Objective criteria to maximize or minimize subject to boundary inequalities.",
            "output_spec": "Optimal decision allocation achieving the theoretical global peak.",
            "when_to_use": [
                "Logistics dispatching, portfolio optimization, resource allocation, and factory production scheduling."
            ],
            "when_not_to_use": [
                "Simple unconstrained problems where elementary calculus or greedy heuristics suffice."
            ],
            "key_takeaway": "Systematically navigates decision boundaries to guarantee mathematically optimal allocations."
        }

    # Universal Fallback for Any CS Algorithm
    return {
        "intuitive_explanation": f"{algorithm_name} is a specialized computational algorithm designed to solve {problem_statement or 'complex computational requirements'}. It systematically evaluates input states, applies strategic decision rules, and produces verified outputs with predictable performance bounds.",
        "paradigm": "Algorithmic Strategy & State Evaluation",
        "key_data_structures": ["Data Buffers", "State Transition Records", "Evaluation Metrics"],
        "input_spec": f"Problem domain inputs and configuration parameters for {algorithm_name}.",
        "output_spec": f"Verified computational solution meeting constraints of {algorithm_name}.",
        "when_to_use": [
            f"When rigorous computational performance and verified logic are required for {algorithm_name}.",
            "High-throughput software architectures needing deterministic execution paths."
        ],
        "when_not_to_use": [
            "Trivial scenarios where simpler linear heuristics or default standard library functions suffice."
        ],
        "key_takeaway": f"Provides structured, repeatable, and scalable problem solving specifically engineered for {algorithm_name}."
    }
