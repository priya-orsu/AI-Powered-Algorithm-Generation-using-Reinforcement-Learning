import re
from typing import Dict, Any
from app.services.ml_encoding_catalog import ML_ENCODING_REGISTRY

# Expanded, comprehensive algorithm definitions and prompt pattern rules (30+ Domains)
ALGORITHM_PROMPT_KNOWLEDGE_BASE = [

    # ------------------ EXTENDED CLASSICAL & MODERN CS ALGORITHMS ------------------
    {
        "name": "Maximum Depth of Binary Tree",
        "category": "Tree & Graph Traversal",
        "keywords": ["maximum depth", "max depth", "maximum depth of binary tree", "maximum depth in bt", "tree depth", "binary tree height", "max depth binary tree", "bt depth"],
        "description": "Finds the maximum depth or height of a binary tree, defined as the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "problem_statement": "Given the root of a binary tree, return its maximum depth using recursive DFS or level-order BFS traversal."
    },
    {
        "name": "Level-Order Tree Traversal",
        "category": "Tree & Graph Traversal",
        "keywords": ["level order traversal", "level order", "binary tree level order", "tree level order traversal", "level order traversal algorithm", "bfs tree traversal", "levelorder"],
        "description": "Traverses a binary tree or graph level by level from root to leaves using a Queue FIFO structure.",
        "problem_statement": "Given a binary tree root, return the level-order traversal of its nodes' values level by level from left to right."
    },
    {
        "name": "Inorder Tree Traversal",
        "category": "Tree & Graph Traversal",
        "keywords": ["inorder traversal", "inorder", "binary tree inorder", "tree inorder traversal", "inorder traversal algorithm", "left root right"],
        "description": "Traverses a binary tree recursively or iteratively in Left-Root-Right order, producing sorted keys for BSTs.",
        "problem_statement": "Given a binary tree root, return the inorder traversal of its nodes' values."
    },
    {
        "name": "Preorder Tree Traversal",
        "category": "Tree & Graph Traversal",
        "keywords": ["preorder traversal", "preorder", "binary tree preorder", "tree preorder traversal", "preorder traversal algorithm", "root left right"],
        "description": "Traverses a binary tree in Root-Left-Right order, useful for creating a copy or prefix expression of a tree.",
        "problem_statement": "Given a binary tree root, return the preorder traversal of its nodes' values."
    },
    {
        "name": "Postorder Tree Traversal",
        "category": "Tree & Graph Traversal",
        "keywords": ["postorder traversal", "postorder", "binary tree postorder", "tree postorder traversal", "postorder traversal algorithm", "left right root"],
        "description": "Traverses a binary tree in Left-Right-Root order, useful for deleting nodes or evaluating postfix expressions.",
        "problem_statement": "Given a binary tree root, return the postorder traversal of its nodes' values."
    },
    {
        "name": "Knuth-Morris-Pratt (KMP) Algorithm",
        "category": "String Matching",
        "keywords": ["kmp", "kmp algorithm", "knuth morris pratt", "knuth-morris-pratt", "lps array", "longest prefix suffix string matching"],
        "description": "Searches for occurrences of a pattern within a main text in linear O(N + M) time using a Partial Match (LPS) table.",
        "problem_statement": "Find all index occurrences of a pattern P in text T in optimal O(|P| + |T|) time without backtracking."
    },
    {
        "name": "LZW Data Compression Algorithm",
        "category": "Data Compression & Encoding",
        "keywords": ["lzw", "lzw compression", "lempel ziv welch", "lzw compression algorithm", "dictionary adaptive compression"],
        "description": "A universal lossless data compression algorithm that builds an adaptive dictionary of recurring character sequences.",
        "problem_statement": "Compress an uncompressed data stream into a sequence of variable-bit dictionary index codes."
    },
    {
        "name": "Disjoint Set Union (DSU / Union-Find)",
        "category": "Advanced Data Structures",
        "keywords": ["union find", "union find algorithm", "disjoint set union", "dsu", "disjoint set", "path compression union by rank"],
        "description": "Maintains a partition of a set into disjoint subsets supporting near O(1) amortized union and find operations.",
        "problem_statement": "Determine connected components and dynamic connectivity in a graph using path compression and union by rank."
    },
    {
        "name": "Topological Sort (Kahn's Algorithm)",
        "category": "Graph Algorithms",
        "keywords": ["topological sort", "topological sorting", "kahn's algorithm", "kahns algorithm", "dag topological order"],
        "description": "Linearly orders vertices of a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, vertex u comes before v.",
        "problem_statement": "Given a DAG, compute a valid linear topological ordering of all vertices in O(V + E) time."
    },
    {
        "name": "Two Pointers Technique",
        "category": "Array & Two Pointers",
        "keywords": ["two pointers", "two pointer", "two pointers algorithm", "opposite pointers", "two pointer technique"],
        "description": "An array algorithmic pattern that uses two memory pointers iterating from opposing ends or at varying speeds to search or partition data in O(N) time.",
        "problem_statement": "Search for target pairs, partitions, or container limits in a sorted array in linear O(N) time using dual index pointers."
    },
    {
        "name": "Sliding Window Algorithm",
        "category": "Array & Two Pointers",
        "keywords": ["sliding window", "sliding window algorithm", "fixed window", "dynamic window", "subarray window sum"],
        "description": "Maintains a continuous window of elements over an array or string to track range metrics in linear O(N) time without recomputing nested loops.",
        "problem_statement": "Find the maximum sum, longest substring, or target range metric across subarrays of size K in O(N) time."
    },
    {
        "name": "Dutch National Flag Algorithm (3-Way Partitioning)",
        "category": "Array & Two Pointers",
        "keywords": ["dutch national flag", "dutch national flag algorithm", "3 way partition", "sort 0s 1s 2s", "dutch flag sort"],
        "description": "Partitions an array of 3 distinct values (0s, 1s, 2s) in single pass linear O(N) time and O(1) space using low, mid, and high pointers.",
        "problem_statement": "Given an array containing only 0s, 1s, and 2s, sort the array in-place in linear O(N) time and O(1) extra space."
    },
    {
        "name": "Floyd's Cycle Detection Algorithm (Tortoise and Hare)",
        "category": "Graph & Linked List Algorithms",
        "keywords": ["floyd cycle detection", "floyd's cycle finding", "tortoise and hare", "tortoise and hare algorithm", "linked list cycle"],
        "description": "Detects cycles in a linked list or sequence using slow and fast pointers moving at different speeds in O(N) time and O(1) space.",
        "problem_statement": "Determine whether a linked list contains a cycle and locate the start node of the loop in O(1) auxiliary space."
    },
    {
        "name": "Coin Change Problem (Dynamic Programming)",
        "category": "Dynamic Programming",
        "keywords": ["coin change", "coin change algorithm", "minimum coins", "coin change problem", "unbounded knapsack coins"],
        "description": "Computes the minimum number of coins needed to make up a target amount of money using dynamic programming subproblem optimization.",
        "problem_statement": "Given an array of coin denominations and a target amount, compute the minimum number of coins needed to make up that amount."
    },
    {
        "name": "Binary Search Tree (BST) Operations",
        "category": "Advanced Data Structures",
        "keywords": ["bst", "bst algorithm", "binary search tree", "binary search tree algorithm", "bst insertion search deletion"],
        "description": "Maintains a node-based binary tree data structure where each node's left key is less than its key and right key is greater, supporting O(log N) operations.",
        "problem_statement": "Perform fast dynamic search, insertion, and deletion operations in expected O(log N) time on a structured binary tree."
    },
    {
        "name": "Ford-Fulkerson Algorithm (Max Flow)",
        "category": "Graph Algorithms",
        "keywords": ["ford fulkerson", "ford fulkerson algorithm", "max flow min cut", "residual graph max flow"],
        "description": "Computes the maximum flow in a flow network by repeatedly finding augmenting paths in the residual graph.",
        "problem_statement": "Calculate the maximum volumetric rate of flow that can pass from source node S to sink node T in a network capacity graph."
    },
    {
        "name": "Dinic's Algorithm (Max Flow)",
        "category": "Graph Algorithms",
        "keywords": ["dinic", "dinics algorithm", "dinic algorithm", "blocking flow network", "level graph max flow"],
        "description": "A fast network flow algorithm that computes max flow in O(V^2 E) time using level graphs and blocking flows via BFS and DFS.",
        "problem_statement": "Compute maximum network flow in a directed graph using level graphs and blocking flow pushes in optimal polynomial time."
    },
    {
        "name": "Manacher's Algorithm",
        "category": "String Processing",
        "keywords": ["manacher", "longest palindromic substring", "linear time palindrome", "palindrome finding"],
        "description": "Finds the longest palindromic substring in any given string in linear O(N) time using palindrome boundary symmetry.",
        "problem_statement": "Given a string s, find the longest palindromic substring in linear O(N) time."
    },
    {
        "name": "Simplex Algorithm",
        "category": "Optimization & Linear Programming",
        "keywords": ["simplex", "linear programming", "lp solver", "linear optimization", "tableau simplex", "dantzig"],
        "description": "A standard method for maximizing or minimizing a linear objective function subject to linear inequality constraints by traversing polytope vertices.",
        "problem_statement": "Find optimal decision variables x to maximize c^T x subject to A x <= b and x >= 0."
    },
    {
        "name": "Hungarian Algorithm",
        "category": "Optimization & Graph Theory",
        "keywords": ["hungarian", "kuhn munkres", "maximum bipartite matching weight", "bipartite assignment", "optimal assignment"],
        "description": "A combinatorial optimization algorithm that solves the assignment problem in polynomial O(N^3) time.",
        "problem_statement": "Find a minimum-cost maximum matching in a complete weighted bipartite graph."
    },
    {
        "name": "Cooley-Tukey Fast Fourier Transform (FFT)",
        "category": "Numerical & Signal Processing",
        "keywords": ["cooley tukey", "fft", "fast fourier transform", "discrete fourier transform", "polynomial multiplication fft"],
        "description": "Computes the Discrete Fourier Transform (DFT) of a sequence in O(N log N) time via divide-and-conquer radix-2 recursion.",
        "problem_statement": "Compute the frequency spectrum or multiply two polynomials of degree N in O(N log N) time."
    },
    {
        "name": "Tarjan's Strongly Connected Components & Bridge Finding",
        "category": "Graph Algorithms",
        "keywords": ["tarjan", "bridge finding", "strongly connected components", "scc", "cut edge", "articulation point", "dfs lowlink"],
        "description": "Finds all strongly connected components or critical bridge edges in a graph in a single DFS pass using discovery times and low-link values.",
        "problem_statement": "Identify all bridges (critical connections) and strongly connected components in a directed or undirected graph in O(V + E) time."
    },
    {
        "name": "Hopcroft-Karp Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["hopcroft karp", "maximum bipartite matching", "unweighted bipartite matching", "augmenting paths"],
        "description": "Computes the maximum cardinality matching in a bipartite graph in O(E * sqrt(V)) time using alternating BFS and DFS phases.",
        "problem_statement": "Find the maximum cardinality matching in a bipartite graph in optimal O(E sqrt(V)) time."
    },
    {
        "name": "Cocktail Shaker Sort",
        "category": "Sorting",
        "keywords": ["cocktail shaker sort", "cocktail sort", "bidirectional bubble sort", "shaker sort", "ripple sort"],
        "description": "A bidirectional variation of Bubble Sort that traverses the list in alternating directions to address turtle elements.",
        "problem_statement": "Sort an array by scanning alternately from left-to-right and right-to-left."
    },
    {
        "name": "Skip List",
        "category": "Advanced Data Structures",
        "keywords": ["skip list", "skiplist", "probabilistic balanced list", "randomized search structure"],
        "description": "A probabilistic alternative to balanced trees that maintains multiple layers of linked nodes to achieve O(log N) search, insert, and delete operations.",
        "problem_statement": "Perform dictionary operations (insert, search, delete) in expected O(log N) time with O(1) pointer updates."
    },
    {
        "name": "Boyer-Moore Majority Voting Algorithm",
        "category": "Array Algorithms",
        "keywords": ["boyer moore voting", "majority element", "majority vote", "linear time majority"],
        "description": "Finds the majority element appearing more than N/2 times in an array in linear O(N) time and O(1) space using candidate counter cancellation.",
        "problem_statement": "Given an array of size n, find the majority element that appears more than n/2 times in O(1) space."
    },
    {
        "name": "Boyer-Moore String Search Algorithm",
        "category": "String Algorithms",
        "keywords": ["boyer moore string search", "bad character heuristic", "good suffix rule", "fast pattern search"],
        "description": "An efficient string-searching algorithm that skips multiple characters using bad character and good suffix shift tables.",
        "problem_statement": "Find all occurrences of a pattern in a text by matching characters from right to left with heuristic skips."
    },
    {
        "name": "Z-Algorithm",
        "category": "String Algorithms",
        "keywords": ["z algorithm", "z array", "string matching z values", "longest prefix match"],
        "description": "Constructs the Z-array for a string of length N in linear O(N) time, where Z[i] is the length of the longest substring starting from s[i] matching the prefix.",
        "problem_statement": "Find all occurrences of pattern P in text T in linear O(|P| + |T|) time."
    },
    {
        "name": "Aho-Corasick Algorithm",
        "category": "String Algorithms",
        "keywords": ["aho corasick", "multi pattern matching", "trie with failure links", "dictionary matching"],
        "description": "A string-searching algorithm that locates elements of a finite set of strings within an input text simultaneously using an augmented Trie.",
        "problem_statement": "Search for multiple dictionary patterns simultaneously in a text stream in linear time."
    },
    {
        "name": "Graham Scan",
        "category": "Computational Geometry",
        "keywords": ["graham scan", "convex hull", "planar points hull", "cross product orientation"],
        "description": "Finds the convex hull of a set of 2D points in O(N log N) time by sorting points by polar angle and maintaining a stack of hull vertices.",
        "problem_statement": "Given a set of 2D coordinates, compute the minimal convex polygon enclosing all points."
    },
    {
        "name": "Strassen's Matrix Multiplication",
        "category": "Numerical Algorithms",
        "keywords": ["strassen", "subcubic matrix multiplication", "divide and conquer matrix"],
        "description": "A sub-cubic matrix multiplication algorithm running in O(N^2.807) time using 7 recursive block multiplications instead of 8.",
        "problem_statement": "Multiply two N x N matrices with asymptotic time complexity strictly faster than standard O(N^3)."
    },
    {
        "name": "Karatsuba Multiplication",
        "category": "Numerical Algorithms",
        "keywords": ["karatsuba", "fast integer multiplication", "divide and conquer multiplication"],
        "description": "A fast multiplication algorithm for large numbers running in O(N^1.585) time by reducing 4 multiplications of N/2 digits to 3.",
        "problem_statement": "Multiply two large N-digit integers in sub-quadratic O(N^1.585) time."
    },
    {
        "name": "Sieve of Eratosthenes",
        "category": "Number Theory",
        "keywords": ["sieve of eratosthenes", "prime generation", "find primes up to n", "prime numbers sieve"],
        "description": "An ancient and highly efficient algorithm for finding all prime numbers up to any given limit in O(N log log N) time.",
        "problem_statement": "Generate all prime numbers strictly less than or equal to a given integer N."
    },
    {
        "name": "Monte Carlo Tree Search (MCTS)",
        "category": "Game Theory & AI",
        "keywords": ["mcts", "monte carlo tree search", "uct", "upper confidence bound trees", "board game search"],
        "description": "A heuristic search algorithm for decision processes, notably used in game playing (Go, Chess) through selection, expansion, simulation, and backpropagation.",
        "problem_statement": "Select the optimal move in a vast combinatorial game tree under incomplete evaluation."
    },
    {
        "name": "Minimax with Alpha-Beta Pruning",
        "category": "Game Theory & AI",
        "keywords": ["minimax", "alpha beta pruning", "adversarial search", "zero sum game tree"],
        "description": "A recursive decision algorithm for two-player zero-sum games that prunes branches that cannot influence the final decision.",
        "problem_statement": "Compute the game-theoretic value and optimal move in a 2-player adversarial game while pruning provably suboptimal subtrees."
    },
    {
        "name": "Deep Q-Network (DQN)",
        "category": "Reinforcement Learning",
        "keywords": ["dqn", "deep q network", "experience replay", "target network", "deep rl"],
        "description": "Combines Q-Learning with deep neural networks, experience replay, and periodic target network updates to learn policies in high-dimensional state spaces.",
        "problem_statement": "Learn an optimal action-value policy Q*(s, a) directly from sensory state observations in complex environments."
    },
    {
        "name": "Proximal Policy Optimization (PPO)",
        "category": "Reinforcement Learning",
        "keywords": ["ppo", "proximal policy optimization", "clipped objective policy", "actor critic rl"],
        "description": "An on-policy reinforcement learning algorithm that alternates between sampling data through interaction and optimizing a clipped surrogate objective function.",
        "problem_statement": "Optimize a continuous or discrete policy without catastrophic policy collapse through surrogate objective clipping."
    },
    {
        "name": "Particle Swarm Optimization (PSO)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["pso", "particle swarm", "swarm intelligence", "velocity position update"],
        "description": "A population-based metaheuristic optimization algorithm inspired by bird flocking, updating particle velocities toward personal best and global best positions.",
        "problem_statement": "Find the global optimum of a non-linear continuous objective function across a multi-dimensional search space."
    },
    {
        "name": "Ant Colony Optimization (ACO)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["aco", "ant colony", "pheromone trail optimization", "dorigo ant routing"],
        "description": "A probabilistic technique for solving computational problems reducible to finding good paths through graphs, inspired by ant foraging behavior.",
        "problem_statement": "Find the shortest tour or optimal routing network via artificial pheromone reinforcement and heuristic visibility."
    },
    {
        "name": "Segment Tree",
        "category": "Advanced Data Structures",
        "keywords": ["segment tree", "range query", "range minimum query", "point update range query", "lazy propagation"],
        "description": "A tree data structure used for storing information about intervals or segments, allowing querying which segment contains a given point in O(log N).",
        "problem_statement": "Support efficient range queries (sum, min, max) and point/range updates in O(log N) time on an array of size N."
    },
    {
        "name": "Fenwick Tree (Binary Indexed Tree)",
        "category": "Advanced Data Structures",
        "keywords": ["fenwick tree", "binary indexed tree", "bit", "prefix sum updates"],
        "description": "A data structure that can efficiently update elements and calculate prefix sums in a table of numbers in O(log N) time.",
        "problem_statement": "Compute dynamic prefix sums and element updates in an array of size N in O(log N) time with O(N) space."
    },

    # ------------------ DYNAMIC PROGRAMMING ------------------
    {
        "name": "Kadane's Algorithm",
        "category": "Dynamic Programming",
        "keywords": ["kadane", "maximum subarray", "max subarray", "max sum subarray", "contiguous subarray sum", "maximum sum array", "greatest sum subarray", "subarray max sum", "largest sum subarray"],
        "description": "Computes the maximum sum of a contiguous subarray within a 1D numeric array in linear O(N) time using dynamic programming state accumulation.",
        "problem_statement": "Given an array of integers, find the contiguous subarray with the largest sum and return its sum."
    },
    {
        "name": "0/1 Knapsack Problem",
        "category": "Dynamic Programming",
        "keywords": ["knapsack", "0/1 knapsack", "item weight capacity optimization", "maximize value weight constraint", "bounded knapsack", "bag capacity max value"],
        "description": "Optimizes total value selection from a set of items with given weights and values subject to a weight capacity constraint.",
        "problem_statement": "Determine the items to include in a collection so that the total weight is less than or equal to a given limit and total value is maximized."
    },
    {
        "name": "Longest Common Subsequence (LCS)",
        "category": "Dynamic Programming",
        "keywords": ["lcs", "longest common subsequence", "common sequence length", "subsequence alignment"],
        "description": "Finds the longest subsequence present in two sequences in the same order but not necessarily contiguous.",
        "problem_statement": "Given two strings, find the length of the longest subsequence present in both strings."
    },
    {
        "name": "Longest Increasing Subsequence (LIS)",
        "category": "Dynamic Programming",
        "keywords": ["lis", "longest increasing subsequence", "increasing elements subsequence", "monotonically increasing subsequence"],
        "description": "Finds the length of the longest subsequence of a given sequence such that all elements of the subsequence are sorted in increasing order.",
        "problem_statement": "Given an unsorted array of integers, find the length of the longest strictly increasing subsequence."
    },
    {
        "name": "Matrix Chain Multiplication",
        "category": "Dynamic Programming",
        "keywords": ["matrix chain multiplication", "optimal matrix parenthesization", "matrix multiplication order", "minimum scalar multiplications"],
        "description": "Determines the most efficient way to multiply a given sequence of matrices together by finding optimal parenthesization.",
        "problem_statement": "Find the optimal order of multiplying a chain of matrices to minimize total scalar multiplications."
    },
    {
        "name": "Coin Change Problem",
        "category": "Dynamic Programming",
        "keywords": ["coin change", "minimum coins", "make change coins", "ways to make amount"],
        "description": "Finds the minimum number of coins needed to make a given total amount of money from a set of coin denominations.",
        "problem_statement": "Given an array of coin denominations and a target amount, compute the fewest coins needed to make up that amount."
    },
    {
        "name": "Edit Distance (Levenshtein Distance)",
        "category": "Dynamic Programming",
        "keywords": ["edit distance", "levenshtein", "string edit distance", "minimum insertion deletion substitution"],
        "description": "Calculates the minimum number of single-character edits (insertions, deletions, substitutions) required to change one word into another.",
        "problem_statement": "Given two strings str1 and str2, find the minimum number of operations to convert str1 to str2."
    },

    # ------------------ SORTING ALGORITHMS ------------------
    {
        "name": "Quick Sort",
        "category": "Sorting",
        "keywords": ["quick sort", "quicksort", "divide and conquer sort", "partition sort", "fastest array sorting", "in-place sorting", "pivot sort"],
        "description": "An efficient, in-place, divide-and-conquer sorting algorithm based on pivot partitioning.",
        "problem_statement": "Sort an array of elements in ascending order by recursively partitioning elements around a pivot."
    },
    {
        "name": "Merge Sort",
        "category": "Sorting",
        "keywords": ["merge sort", "mergesort", "stable divide and conquer sort", "stable sorting", "external sorting"],
        "description": "A stable divide-and-conquer sorting algorithm that divides input into equal halves, sorts them, and merges them.",
        "problem_statement": "Sort a dataset stably with guaranteed O(N log N) time complexity by recursively splitting and merging halves."
    },
    {
        "name": "Heap Sort",
        "category": "Sorting",
        "keywords": ["heap sort", "heapsort", "priority queue sort", "binary heap sort", "in-place max heap sort"],
        "description": "A comparison-based sorting algorithm that uses a binary heap data structure to sort elements in O(N log N) time.",
        "problem_statement": "Sort an array by building a Max-Heap and repeatedly extracting the maximum element."
    },
    {
        "name": "Bubble Sort",
        "category": "Sorting",
        "keywords": ["bubble sort", "bubblesort", "adjacent swap sort", "simple sorting"],
        "description": "A simple comparison sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if out of order.",
        "problem_statement": "Sort an array by iteratively swapping adjacent elements until the list is fully sorted."
    },
    {
        "name": "Insertion Sort",
        "category": "Sorting",
        "keywords": ["insertion sort", "insertionsort", "card sorting", "incremental sorting"],
        "description": "Builds the final sorted array one item at a time by inserting unsorted elements into their correct position in the sorted sub-list.",
        "problem_statement": "Iteratively insert each element into its proper position within a sorted portion of the array."
    },
    {
        "name": "Selection Sort",
        "category": "Sorting",
        "keywords": ["selection sort", "selectionsort", "find min element swap"],
        "description": "Sorts an array by repeatedly finding the minimum element from the unsorted part and putting it at the beginning.",
        "problem_statement": "Sort an array by selecting the smallest element from the unsorted section and placing it at the boundary."
    },
    {
        "name": "Counting Sort",
        "category": "Sorting",
        "keywords": ["counting sort", "countingsort", "non-comparison sort", "frequency array sort", "linear time sort", "count sort"],
        "description": "A non-comparison integer sorting algorithm that operates in linear O(N + K) time by counting frequencies of key values within a specific range.",
        "problem_statement": "Sort an array of non-negative integers by counting the occurrence of each unique key value and computing prefix indices."
    },
    {
        "name": "Radix Sort",
        "category": "Sorting",
        "keywords": ["radix sort", "radixsort", "digit by digit sort", "lsb msb sort", "non-comparison digit sort"],
        "description": "A non-comparison sorting algorithm that sorts data with integer keys by grouping keys by individual digits sharing position and value.",
        "problem_statement": "Sort an array of numbers by processing individual digits from least significant to most significant using stable counting sort passes."
    },
    {
        "name": "Bucket Sort",
        "category": "Sorting",
        "keywords": ["bucket sort", "bucketsort", "bin sort", "scatter gather sort", "floating point sorting"],
        "description": "A distribution sorting algorithm that partitions an array into a set of buckets, sorts each bucket individually, and concatenates the buckets.",
        "problem_statement": "Sort uniformly distributed floating-point numbers by partitioning elements into sub-range buckets and merging sorted buckets."
    },

    # ------------------ SEARCHING & STRINGS ------------------
    {
        "name": "Binary Search",
        "category": "Searching",
        "keywords": ["binary search", "binarysearch", "search in sorted array", "logarithmic search", "half interval search"],
        "description": "Finds the position of a target value within a sorted array using logarithmic O(log N) search space division.",
        "problem_statement": "Search for a target value in a sorted array by repeatedly dividing the search interval in half."
    },
    {
        "name": "Linear Search",
        "category": "Searching",
        "keywords": ["linear search", "sequential search", "search unsorted array", "find element sequentially"],
        "description": "Sequentially checks each element of the list until a match is found or the whole list has been searched.",
        "problem_statement": "Search for a target element in an unsorted list by checking elements one by one."
    },
    {
        "name": "KMP String Matching Algorithm",
        "category": "String Matching",
        "keywords": ["kmp", "knuth morris pratt", "pattern matching in text", "string search prefix table", "lps array search"],
        "description": "Searches for occurrences of a pattern within a main text string using a precompiled Longest Prefix Suffix (LPS) array in linear time.",
        "problem_statement": "Find all occurrences of a pattern P in text T in O(N + M) time without backtracking text pointers."
    },
    {
        "name": "Rabin-Karp Algorithm",
        "category": "String Matching",
        "keywords": ["rabin karp", "rabinkarp", "rolling hash search", "string matching rolling hash"],
        "description": "Uses rolling hash functions to quickly search for occurrences of a pattern in a text string.",
        "problem_statement": "Find pattern matches in a text by comparing rolling hash values of text windows."
    },

    # ------------------ GRAPH ALGORITHMS ------------------
    {
        "name": "Network Path Routing Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["routing", "network routing", "packet routing", "route optimization", "router algorithm", "data routing", "path routing", "network path"],
        "description": "Calculates shortest and lowest-latency data transmission routes across network routers and graph nodes using dynamic link-state and vector metrics.",
        "problem_statement": "Determine the optimal, minimum-cost routing path for transmitting data packets across network routers or graph nodes without packet loss."
    },
    {
        "name": "Dijkstra's Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["dijkstra", "shortest path graph", "single source shortest path", "weighted graph path", "gps routing", "minimum cost path", "route finder"],
        "description": "Determines the shortest path between nodes in a graph with non-negative edge weights using a priority queue.",
        "problem_statement": "Find the shortest paths from a single source node to all other vertices in a weighted graph without negative edges."
    },
    {
        "name": "Bellman-Ford Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["bellman ford", "bellmanford", "negative weight edge shortest path", "negative cycle detection"],
        "description": "Computes shortest paths from a single source vertex to all other vertices in a weighted digraph, supporting negative edge weights.",
        "problem_statement": "Find single-source shortest paths in a graph with arbitrary edge weights and detect negative weight cycles."
    },
    {
        "name": "Floyd-Warshall Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["floyd warshall", "floydwarshall", "all pairs shortest path", "apsp graph"],
        "description": "Finds shortest paths between all pairs of vertices in a weighted graph using dynamic programming state transitions.",
        "problem_statement": "Compute the shortest path distances between all pairs of vertices in a directed weighted graph."
    },
    {
        "name": "A* Search Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["a* search", "a star", "heuristic pathfinding", "pathfinding grid AI", "a star search"],
        "description": "An informed search algorithm that uses heuristic distance functions to find the shortest path from start to goal.",
        "problem_statement": "Find the shortest path on a graph or grid using distance cost f(n) = g(n) + h(n)."
    },
    {
        "name": "Kruskal's Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["kruskal", "minimum spanning tree", "mst kruskal", "greedy minimum spanning tree", "disjoint set mst"],
        "description": "A greedy algorithm that finds a minimum spanning tree for a connected weighted graph by sorting edges and using Disjoint-Set (Union-Find).",
        "problem_statement": "Find the subset of edges that connects all vertices in a weighted graph with minimum total weight, avoiding cycles."
    },
    {
        "name": "Prim's Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["prim", "prims algorithm", "mst prim", "vertex growing minimum spanning tree"],
        "description": "A greedy algorithm that finds a minimum spanning tree for a weighted undirected graph by expanding a growing subtree.",
        "problem_statement": "Grow a minimum spanning tree node by node selecting the minimum weight connecting edge."
    },
    {
        "name": "Breadth First Search (BFS)",
        "category": "Graph Algorithms",
        "keywords": ["bfs", "breadth first search", "level order traversal", "shortest path unweighted graph", "queue graph traversal"],
        "description": "Traverses or searches graph or tree data structures level by level using a queue.",
        "problem_statement": "Explore all vertices at the present depth before moving on to vertices at the next depth level."
    },
    {
        "name": "Depth First Search (DFS)",
        "category": "Graph Algorithms",
        "keywords": ["dfs", "depth first search", "stack graph traversal", "backtracking traversal", "tree depth exploration"],
        "description": "Traverses graph or tree data structures by exploring as far as possible along each branch before backtracking.",
        "problem_statement": "Explore graph vertices deeply along each branch using a call stack or explicit stack until backtracking is required."
    },
    {
        "name": "Topological Sort",
        "category": "Graph Algorithms",
        "keywords": ["topological sort", "topological sorting", "kahn algorithm", "dag ordering", "dependency resolution"],
        "description": "Orders the vertices of a Directed Acyclic Graph (DAG) linearly such that for every directed edge u -> v, vertex u comes before v.",
        "problem_statement": "Produce a linear ordering of vertices in a DAG to resolve task dependencies."
    },
    {
        "name": "Cycle Detection in Graph",
        "category": "Graph Algorithms",
        "keywords": ["cycle detection", "detect cycle graph", "loop detection in graph", "graph cycle check"],
        "description": "Determines whether a graph contains any cycles using DFS recursion stack states or Kahn's BFS algorithm.",
        "problem_statement": "Check if a directed or undirected graph contains at least one cycle."
    },

    # ------------------ MATHEMATICS & FUNDAMENTALS ------------------
    {
        "name": "Euclidean Algorithm (GCD / LCM)",
        "category": "Mathematics",
        "keywords": ["gcd", "greatest common divisor", "euclidean algorithm", "lcm", "least common multiple", "hcf"],
        "description": "Computes the Greatest Common Divisor (GCD) of two integers efficiently using modulo reduction.",
        "problem_statement": "Compute the greatest common divisor of two integers a and b using repeated remainder reduction."
    },
    {
        "name": "Sieve of Eratosthenes",
        "category": "Mathematics",
        "keywords": ["sieve of eratosthenes", "prime numbers up to n", "find prime numbers", "generate primes", "prime sieve"],
        "description": "An ancient, highly efficient algorithm for finding all prime numbers up to a specified integer N.",
        "problem_statement": "Find all prime numbers less than or equal to a given number N by iteratively marking composite numbers."
    },
    {
        "name": "Fast Exponentiation (Binary Exponentiation)",
        "category": "Mathematics",
        "keywords": ["fast exponentiation", "binary exponentiation", "power function", "calculate a^b", "modulo exponentiation"],
        "description": "Computes a^b in logarithmic O(log B) time by squaring the base and halving the exponent.",
        "problem_statement": "Calculate a raised to the power b efficiently using binary decomposition of the exponent."
    },
    {
        "name": "Fibonacci Sequence",
        "category": "Fundamentals",
        "keywords": ["fibonacci", "fibanocci", "fibonacci series", "fibonacci numbers", "nth fibonacci number"],
        "description": "Calculates numbers in the Fibonacci sequence where each number is the sum of the two preceding ones.",
        "problem_statement": "Compute the Nth number in the Fibonacci sequence using iterative, recursive, or dynamic programming approaches."
    },
    {
        "name": "Factorial Calculation",
        "category": "Fundamentals",
        "keywords": ["factorial", "factorical", "n factorial", "product of integers 1 to n"],
        "description": "Computes the product of all positive integers less than or equal to a given non-negative integer n.",
        "problem_statement": "Compute N! (N factorial), which is the product of all positive integers from 1 to N."
    },
    {
        "name": "Palindrome Check",
        "category": "Fundamentals",
        "keywords": ["palindrome", "check palindrome", "palindrome string", "palindrome number"],
        "description": "Verifies whether a string or sequence reads the same forwards and backwards using two-pointer comparison.",
        "problem_statement": "Check if a given string or number is a palindrome."
    },
    {
        "name": "String Reversal",
        "category": "Fundamentals",
        "keywords": ["reverse string", "reverse array", "reverse sequence", "invert string characters", "string flip"],
        "description": "Reverses the order of characters in a string or elements in a 1D sequence in O(N) time.",
        "problem_statement": "Reverse a given sequence or string in-place or into a new data structure."
    },

    # ------------------ ARRAY & TWO POINTERS ALGORITHMS ------------------
    {
        "name": "Move Zeroes Algorithm",
        "category": "Array & Two Pointers",
        "keywords": ["move zeroes", "move zeros", "move zeroes to end", "move zeros to end", "push zeroes to end", "push zeros to end", "shift zeroes", "shift zeros", "zeroes to end", "zeros to end", "zero to end"],
        "description": "Moves all zero elements in an array to the end while maintaining the relative order of non-zero elements in linear O(N) time and O(1) space.",
        "problem_statement": "Given an integer array, move all 0s to the end of it while maintaining the relative order of the non-zero elements in-place."
    },
    {
        "name": "Two-Pointer Algorithm",
        "category": "Array & Two Pointers",
        "keywords": ["two pointer", "two pointers", "two pointer technique", "left right pointer", "in-place array swap", "opposite direction pointers"],
        "description": "An efficient array searching and partitioning technique using two indices moving towards or away from each other to solve linear search problems in O(N) time.",
        "problem_statement": "Process elements of an array using two pointer variables moving across indices to satisfy target constraints."
    },
    {
        "name": "Sliding Window Technique",
        "category": "Array & Two Pointers",
        "keywords": ["sliding window", "sliding window technique", "subarray window", "maximum sum subarray of size k", "fixed window search", "dynamic window search"],
        "description": "A dynamic array partitioning technique that tracks a contiguous subarray window to solve range queries in linear O(N) time.",
        "problem_statement": "Find optimal contiguous subarray metrics (max sum, min length) by expanding and contracting window boundaries."
    },
    {
        "name": "Dutch National Flag Algorithm",
        "category": "Array & Two Pointers",
        "keywords": ["dutch national flag", "sort colors", "0 1 2 sort", "three way partitioning", "3-way partition"],
        "description": "Partitions an array containing three distinct keys (e.g. 0s, 1s, 2s) into three segments in linear O(N) time using three pointers.",
        "problem_statement": "Sort an array of 0s, 1s, and 2s in-place using a single pass with low, mid, and high pointers."
    },
    # ------------------ DATABASE & INDEXING ALGORITHMS ------------------
    {
        "name": "B-Tree Indexing Algorithm",
        "category": "Database & Indexing",
        "keywords": ["database", "db index", "database index", "database indexing", "b-tree", "btree", "b tree", "b-tree indexing", "b tree search", "db search algorithm"],
        "description": "A self-balancing M-way search tree algorithm used in database management systems to optimize block-based storage reads and indexing in O(log N) time.",
        "problem_statement": "Efficiently locate, insert, and delete records in block storage using a balanced multi-way tree structure."
    },
    {
        "name": "B+ Tree Indexing Algorithm",
        "category": "Database & Indexing",
        "keywords": ["b+ tree", "b+tree", "b plus tree", "b+ tree indexing", "range query indexing", "clustered index"],
        "description": "A refined B-Tree variation where all records reside in linked leaf nodes, optimizing multi-key sequential range scans and database indexing.",
        "problem_statement": "Execute fast equality lookups and range scans on database storage using doubly-linked leaf block nodes."
    },
    {
        "name": "Hash Indexing Algorithm",
        "category": "Database & Indexing",
        "keywords": ["hash index", "hash indexing", "hash table database index", "equality database index", "bucket index"],
        "description": "Direct directory lookup algorithm using hash functions to achieve O(1) constant-time exact match index search in relational and key-value databases.",
        "problem_statement": "Map database keys to storage bucket offsets using hash functions for O(1) equality query execution."
    },
    {
        "name": "LSM-Tree Indexing Algorithm",
        "category": "Database & Indexing",
        "keywords": ["lsm tree", "lsm-tree", "log-structured merge-tree", "write-optimized indexing", "rocksdb index"],
        "description": "A write-optimized database indexing algorithm that buffers mutations in memory (MemTable) before flushing to sorted disk SSTables.",
        "problem_statement": "Handle ultra-high write throughput in databases using memory buffer tables and asynchronous SSTable disk compaction."
    },

    # ------------------ METAHEURISTIC & EVOLUTIONARY ALGORITHMS ------------------
    {
        "name": "Simulated Annealing (SA)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["simulated annealing", "annealing", "sa optimization", "thermal cooling search", "probabilistic hill climbing", "cooling schedule optimization", "metaheuristic annealing"],
        "description": "A probabilistic metaheuristic inspired by metal annealing that escapes local optima by accepting worse solutions with probability proportional to temperature.",
        "problem_statement": "Optimize a continuous or combinatorial objective function by iteratively exploring neighborhood states with temperature cooling schedule T(k)."
    },
    {
        "name": "Particle Swarm Optimization (PSO)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["particle swarm optimization", "particle swarm", "pso", "swarm intelligence", "swarm optimization", "velocity position update", "pbest gbest search"],
        "description": "A swarm intelligence metaheuristic that optimizes problem candidates by moving particles through parameter space based on personal and global best positions.",
        "problem_statement": "Find optimal solution vectors by updating particle velocities v_i and positions x_i driven by cognitive and social acceleration coefficients."
    },
    {
        "name": "Genetic Algorithm (GA)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["genetic algorithm", "genetic algorithms", "ga optimization", "chromosome crossover mutation", "population evolution", "natural selection algorithm", "fitness selection"],
        "description": "An evolutionary metaheuristic algorithm that mimics natural selection using population encoding, selection, crossover, and mutation operators.",
        "problem_statement": "Evolve a population of candidate solution chromosomes over multiple generations to maximize composite fitness score."
    },
    {
        "name": "Ant Colony Optimization (ACO)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["ant colony optimization", "ant colony", "aco", "pheromone trail search", "ant system", "graph path pheromone"],
        "description": "A swarm intelligence metaheuristic based on ant foraging behavior using artificial pheromone trails to discover optimal graph paths.",
        "problem_statement": "Find shortest or lowest-cost paths in a graph by simulating ants depositing and evaporating pheromone intensity."
    },
    # ------------------ PUZZLE & CONSTRAINT SATISFACTION ------------------
    {
        "name": "N-Queens & Backtracking Puzzle Algorithm",
        "category": "Puzzle & Constraint Satisfaction",
        "keywords": ["puzzle", "puzzle algorithm", "backtracking puzzle", "n-queens", "n queens", "sudoku", "grid puzzle", "8-puzzle", "sliding puzzle", "constraint satisfaction", "puzzle solver"],
        "description": "Solves complex constraint satisfaction puzzles and grid problems using recursive state-space exploration and intelligent branch pruning.",
        "problem_statement": "Find a valid state configuration or placement grid satisfying all problem constraints without conflicts (e.g. non-attacking N-Queens placement)."
    },
    {
        "name": "Traveling Salesperson Problem (TSP)",
        "category": "Puzzle & Constraint Satisfaction",
        "keywords": ["tsp", "traveling salesman", "traveling salesperson", "tour optimization", "salesman problem", "shortest tour", "travelling salesman"],
        "description": "Finds the shortest possible route that visits a set of cities exactly once and returns to the origin city using 2-Opt heuristic local search.",
        "problem_statement": "Determine the minimum-cost closed tour visiting N cities exactly once given an inter-city distance matrix."
    },
    {
        "name": "Tabu Search (TS)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["tabu search", "tabu", "ts optimization", "tabu memory list", "neighborhood search prohibition", "local search memory"],
        "description": "A metaheuristic local search method that uses a memory list of prohibited moves (tabu list) to avoid cycling and escape local minima.",
        "problem_statement": "Navigate complex solution spaces by exploring non-tabu neighborhood moves while maintaining flexible short-term memory tenure."
    },
    {
        "name": "Grey Wolf Optimizer (GWO)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["grey wolf optimizer", "grey wolf", "gwo", "wolf pack hunting", "alpha beta delta wolf", "pack hierarchy optimization"],
        "description": "A nature-inspired metaheuristic mimicking the leadership hierarchy and hunting mechanism of grey wolves (Alpha, Beta, Delta, Omega).",
        "problem_statement": "Optimize multi-dimensional search spaces by simulating encircling, hunting, and attacking behaviors led by elite wolves."
    },
    # ------------------ REAL-WORLD APPLICATION DOMAINS ------------------
    {
        "name": "Clinical Risk Scoring & Patient Triage Algorithm",
        "category": "Healthcare & Biomedical CS",
        "keywords": ["healthcare", "healthcare algorithm", "used healthcare algorithm", "medical", "clinical", "patient triage", "hospital", "diagnosis", "biomedical", "disease risk"],
        "description": "Computes patient disease risk scores, survival probabilities, and clinical triage urgency using multi-feature risk factor stratification and priority queues.",
        "problem_statement": "Stratify patient vital signs, lab metrics, and clinical risk factors to calculate diagnostic risk scores and allocate ICU/triage priority in real time."
    },
    {
        "name": "Portfolio Optimization & Financial Risk Analysis Algorithm",
        "category": "Finance & Algorithmic Trading",
        "keywords": ["finance", "finance algorithm", "financial", "stock", "trading", "portfolio optimization", "sharpe ratio", "risk management", "black scholes", "markowitz"],
        "description": "Optimizes asset weight allocations across financial portfolios to maximize expected return while minimizing portfolio volatility and Value-at-Risk (VaR).",
        "problem_statement": "Determine optimal portfolio asset weight vectors w that maximize Sharpe ratio subject to risk variance boundaries."
    },
    {
        "name": "Kinematic Path Planning & SLAM Algorithm",
        "category": "Robotics & Autonomous Systems",
        "keywords": ["robotics", "robotics algorithm", "robot", "drone", "autonomous", "slam", "path planning", "rrt", "motion planning", "kinematic"],
        "description": "Constructs collision-free motion trajectories and builds spatial maps for autonomous mobile robots navigating dynamic environments.",
        "problem_statement": "Compute continuous joint-space control commands driving a robotic agent from start state S to target G while avoiding obstacles."
    },
    {
        "name": "RSA Encryption & Cryptographic Hash Algorithm",
        "category": "Cybersecurity & Cryptography",
        "keywords": ["security", "security algorithm", "crypto", "cryptography", "encryption", "rsa", "aes", "hash function", "digital signature", "cipher"],
        "description": "Secures data transmission using asymmetric prime factorization key pairs and cryptographic hash digests.",
        "problem_statement": "Encrypt plaintext messages using public key exponentiation C = M^e mod N and verify digital signatures against tamper-proof hashes."
    },
    {
        "name": "Collaborative Filtering & Matrix Factorization Algorithm",
        "category": "Recommendation Systems",
        "keywords": ["recommendation", "recommendation algorithm", "recommender", "movie recommendation", "collaborative filtering", "matrix factorization", "svd", "user rating"],
        "description": "Predicts user preferences and generates personalized item recommendations by decomposing sparse user-item interaction matrices.",
        "problem_statement": "Decompose sparse interaction matrix R ≈ U · V^T to predict unobserved user rating scores for unrated items."
    },
    {
        "name": "Convolutional Feature Extraction & Spatial Filtering Algorithm",
        "category": "Computer Vision & Image Processing",
        "keywords": ["image processing", "image algorithm", "computer vision", "vision algorithm", "canny edge", "sobel filter", "object detection", "feature extraction"],
        "description": "Processes 2D image matrix pixels using spatial convolution kernels to detect structural boundaries and feature representations.",
        "problem_statement": "Apply 2D spatial convolution kernels over image pixel matrices to compute gradient magnitudes and detect object contours."
    }
,
    {
        "name": "Simple Genetic Algorithm (SGA)",
        "category": "Metaheuristic & Evolutionary Algorithms",
        "keywords": ["sga", "simple genetic algorithm", "binary genetic algorithm", "roulette wheel selection", "single point crossover", "holland ga", "bit flip mutation"],
        "description": "Foundational binary-encoded genetic algorithm implementing Holland's schema theorem, fitness-proportionate roulette wheel selection, single-point crossover, and bit-flip mutation.",
        "problem_statement": "Optimize a continuous non-linear mathematical objective function f(x) over a bounded interval using binary chromosome encoding."
    },
    {
        "name": "Genetic Algorithm for TSP (GA-TSP)",
        "category": "Combinatorial Optimization",
        "keywords": ["ga-tsp", "ga tsp", "tsp genetic", "genetic algorithm for tsp", "traveling salesperson genetic", "ordered crossover", "ox crossover", "permutation ga", "tour optimization"],
        "description": "Permutation-based genetic algorithm designed to solve the NP-hard Traveling Salesperson Problem using Ordered Crossover (OX) and Inversion Mutation.",
        "problem_statement": "Find the shortest possible closed tour visiting each of N cities exactly once and returning to the starting point."
    },
    {
        "name": "Genetic Algorithm for 0/1 Knapsack (GA-Knapsack)",
        "category": "Constrained Optimization",
        "keywords": ["ga-knapsack", "ga knapsack", "knapsack genetic", "genetic algorithm for knapsack", "penalty knapsack", "0/1 knapsack ga", "constrained genetic algorithm", "0/1 knapsack"],
        "description": "Constraint-handling genetic algorithm for the 0/1 Knapsack problem using dynamic penalty coefficients, uniform crossover, and elitism.",
        "problem_statement": "Maximize total profit value of packed items subject to a strict maximum weight capacity limit W using binary inclusion genes."
    },
    {
        "name": "NSGA-II Multi-Objective Genetic Algorithm",
        "category": "Multi-Objective Optimization",
        "keywords": ["nsga-ii", "nsga2", "nsga ii", "multi-objective genetic", "pareto genetic", "fast non-dominated sorting", "crowding distance", "deb algorithm", "pareto optimal front"],
        "description": "Elite state-of-the-art multi-objective evolutionary algorithm employing fast non-dominated sorting O(M*N^2) and crowding distance diversity preservation.",
        "problem_statement": "Simultaneously optimize multiple conflicting objective functions f1(x) and f2(x) to approximate the global Pareto-optimal frontier."
    },
    {
        "name": "Differential Evolution (DE)",
        "category": "Evolutionary Computation",
        "keywords": ["differential evolution", "de algorithm", "de/rand/1/bin", "difference vector mutation", "continuous evolution", "storn price", "differential optimization"],
        "description": "Stochastically robust population-based continuous parameter optimizer that mutates individuals using scaled vector differences.",
        "problem_statement": "Find the global minimum of a non-differentiable, non-linear continuous objective function f(x) in D-dimensional real space R^D."
    },
    {
        "name": "Island Model Parallel Genetic Algorithm",
        "category": "Distributed Evolutionary Algorithms",
        "keywords": ["island model", "island model genetic algorithm", "parallel genetic algorithm", "subpopulation migration", "ring topology ga", "parallel ga", "multi-island ga"],
        "description": "Coarse-grained parallel genetic algorithm partitioning the global population into isolated sub-populations that evolve independently with periodic migration.",
        "problem_statement": "Scale evolutionary search across multi-core distributed architectures while avoiding premature convergence in complex multimodal landscapes."
    },
    {
        "name": "Adaptive Genetic Algorithm (AGA)",
        "category": "Self-Adaptive Optimization",
        "keywords": ["adaptive genetic algorithm", "aga", "dynamic crossover", "adaptive mutation", "srinivas patnaik", "self-adaptive ga", "dynamic probability ga"],
        "description": "Dynamically regulated evolutionary algorithm implementing the Srinivas-Patnaik formulation to automatically adjust crossover and mutation probabilities in real-time.",
        "problem_statement": "Dynamically maintain an optimal balance between global exploration and local exploitation throughout generations without manual tuning."
    },
    # ------------------ ADVANCED SEARCH & WEB ALGORITHMS ------------------
    {
        "name": "PageRank Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["pagerank", "page rank", "google pagerank", "link analysis algorithm", "web graph ranking", "random surfer model", "eigenvector centrality", "web ranking"],
        "description": "Measures the relative importance of website nodes in a hyperlink graph by computing the stationary probability distribution of a random surfer model with damping factor.",
        "problem_statement": "Assign numerical weighting scores to each element of a hyperlinked set of documents to measure its relative importance within the network."
    },
    {
        "name": "Bloom Filter",
        "category": "Data Structures & Hashing",
        "keywords": ["bloom filter", "bloomfilter", "probabilistic data structure", "membership test", "space efficient filter", "bit array hash"],
        "description": "A space-efficient probabilistic data structure used to test whether an element is a member of a set, allowing false positives but zero false negatives.",
        "problem_statement": "Test set membership with extremely low memory overhead using multiple independent hash functions over a compact bit array."
    },
    {
        "name": "Convex Hull (Graham Scan)",
        "category": "Computational Geometry",
        "keywords": ["convex hull", "graham scan", "jarvis march", "gift wrapping", "convex boundary", "minimal convex polygon", "computational geometry", "quickhull"],
        "description": "Finds the smallest convex polygon containing all points in a 2D plane by sorting points by polar angle and processing candidate vertices via stack.",
        "problem_statement": "Given a set of n points in the plane, find the subset of vertices that forms the smallest convex polygon enclosing all points in O(N log N) time."
    },
    {
        "name": "K-Means Clustering",
        "category": "Machine Learning",
        "keywords": ["kmeans", "k-means", "k means", "k means clustering", "centroid clustering", "unsupervised clustering", "cluster points", "data clustering"],
        "description": "An unsupervised vector quantization algorithm that partitions n observations into k clusters where each point belongs to the cluster with the nearest centroid.",
        "problem_statement": "Iteratively partition data points into K clusters to minimize within-cluster variance (sum of squared Euclidean distances to cluster centroids)."
    },
    {
        "name": "Trie (Prefix Tree)",
        "category": "Data Structures & String Matching",
        "keywords": ["trie", "prefix tree", "radix tree", "autocomplete data structure", "dictionary tree", "trie search", "trie tree"],
        "description": "An M-ary tree data structure used for storing and retrieving strings over an alphabet, optimized for fast prefix lookup and auto-completion.",
        "problem_statement": "Store a dictionary of strings such that search, insertion, and prefix matching can be executed in O(L) time where L is the key length."
    },
    {
        "name": "AVL Tree",
        "category": "Data Structures & Trees",
        "keywords": ["avl tree", "avl", "balanced binary search tree", "avl rotation", "self-balancing bst", "height balanced tree"],
        "description": "A self-balancing binary search tree where the difference between heights of left and right subtrees (balance factor) cannot exceed one for any node.",
        "problem_statement": "Maintain strictly balanced tree height of O(log N) after insertions and deletions using single and double tree rotations."
    },
    {
        "name": "Red-Black Tree",
        "category": "Data Structures & Trees",
        "keywords": ["red black tree", "red-black tree", "rb tree", "self-balancing tree", "color rotation tree", "red black bst"],
        "description": "A self-balancing binary search tree that uses node color bits (red/black) and rotation properties to ensure no simple path is more than twice as long as any other.",
        "problem_statement": "Guarantee logarithmic O(log N) search, insertion, and deletion times in a search tree through color constraints and tree rotations."
    },
    {
        "name": "Segment Tree",
        "category": "Data Structures & Range Queries",
        "keywords": ["segment tree", "range query tree", "range minimum query", "rmq", "range sum segment tree"],
        "description": "A binary tree used for storing intervals or segments, allowing fast range queries and point updates in O(log N) time.",
        "problem_statement": "Execute range queries (e.g. sum, min, max) and array element updates over arbitrary intervals in O(log N) time."
    },
    {
        "name": "Fenwick Tree (Binary Indexed Tree)",
        "category": "Data Structures & Range Queries",
        "keywords": ["fenwick tree", "binary indexed tree", "bit tree", "prefix sum tree", "fenwick", "bit range query"],
        "description": "A compact array-based data structure that can efficiently update elements and calculate prefix sums in a table of numbers in O(log N) time.",
        "problem_statement": "Compute prefix sum queries and perform point value updates in a sequence of N numbers using bitwise two's complement indexing."
    },
    {
        "name": "Disjoint Set Union (Union-Find)",
        "category": "Data Structures & Graphs",
        "keywords": ["dsu", "union find", "disjoint set", "disjoint set union", "path compression", "union by rank", "connected components dsu"],
        "description": "A data structure that stores a collection of disjoint sets and supports near constant time operations: find representative and union sets.",
        "problem_statement": "Track partition of an element universe into non-overlapping subsets and determine connectivity between elements in near-constant time."
    },
    {
        "name": "Tarjan's Strongly Connected Components (SCC)",
        "category": "Graph Algorithms",
        "keywords": ["tarjan", "tarjan scc", "strongly connected components", "low link values", "scc decomposition", "tarjan's algorithm"],
        "description": "Finds all strongly connected components in a directed graph in linear O(V + E) time using DFS recursion and a stack of discovered vertices.",
        "problem_statement": "Decompose a directed graph into maximal subgraphs where every vertex is reachable from every other vertex in the subgraph."
    },
    {
        "name": "Kosaraju's Algorithm",
        "category": "Graph Algorithms",
        "keywords": ["kosaraju", "kosaraju scc", "transpose graph scc", "strongly connected components kosaraju", "kosaraju's algorithm"],
        "description": "Computes strongly connected components of a directed graph in linear O(V + E) time using two DFS passes and graph transposition.",
        "problem_statement": "Partition vertices of a directed graph into maximal strongly connected subgraphs using forward and reversed graph traversals."
    },
    {
        "name": "Ford-Fulkerson Algorithm (Max Flow)",
        "category": "Graph Algorithms",
        "keywords": ["ford fulkerson", "max flow", "maximum flow", "min cut", "augmenting path", "residual graph", "edmonds karp", "network flow"],
        "description": "Computes the maximum flow in a flow network by repeatedly finding augmenting paths in the residual graph until no path exists.",
        "problem_statement": "Determine the maximum amount of flow that can pass from source s to sink t through a capacitated directed network."
    },
    {
        "name": "Boyer-Moore String Search",
        "category": "String Matching",
        "keywords": ["boyer moore", "boyer-moore", "bad character rule", "good suffix rule", "fast pattern search", "boyer moore algorithm"],
        "description": "A highly efficient string-searching algorithm that skips large sections of the text by comparing characters from right to left using precomputed shift tables.",
        "problem_statement": "Locate occurrences of a pattern P within text T in sub-linear expected time using bad character and good suffix heuristic shifts."
    },
    {
        "name": "Huffman Coding",
        "category": "Greedy Algorithms",
        "keywords": ["huffman coding", "huffman", "huffman tree", "lossless compression", "prefix codes", "frequency tree compression"],
        "description": "A lossless data compression entropy encoding algorithm that assigns variable-length binary prefix codes based on character frequencies using a min-heap.",
        "problem_statement": "Construct an optimal prefix code tree to minimize total encoded bit length of a message based on character frequency distribution."
    },
    {
        "name": "Activity Selection Problem",
        "category": "Greedy Algorithms",
        "keywords": ["activity selection", "interval scheduling", "activity scheduling", "maximum non overlapping activities", "greedy interval"],
        "description": "Selects the maximum number of mutually compatible activities that can be performed by a single person or machine using greedy sorting by finish times.",
        "problem_statement": "Given n activities with start and finish times, select the maximum size subset of mutually non-overlapping activities."
    },
    {
        "name": "Job Sequencing with Deadlines",
        "category": "Greedy Algorithms",
        "keywords": ["job sequencing", "job scheduling deadlines", "greedy job profit", "slot allocation jobs"],
        "description": "Greedy algorithm that schedules jobs with execution deadlines and profits to maximize total profit, completing jobs before their deadlines.",
        "problem_statement": "Given a set of jobs with associated deadlines and profits, find the sequencing that yields the maximum possible total profit."
    },
    {
        "name": "Shell Sort",
        "category": "Sorting",
        "keywords": ["shell sort", "shellsort", "diminishing increment sort", "gap sequence sort"],
        "description": "An in-place comparison sort that generalizes insertion sort by comparing elements separated by a diminishing gap sequence.",
        "problem_statement": "Sort an array by sorting elements at fixed intervals and progressively reducing intervals until the gap is 1."
    },
    {
        "name": "TimSort",
        "category": "Sorting",
        "keywords": ["timsort", "tim sort", "hybrid sort", "python sorting algorithm", "natural merge sort"],
        "description": "An adaptive, stable hybrid sorting algorithm derived from merge sort and insertion sort, designed to perform efficiently on real-world data with natural runs.",
        "problem_statement": "Sort real-world collections stably and adaptively with O(N log N) worst case and O(N) best case on partially ordered sequences."
    },
    {
        "name": "Two Sum Problem",
        "category": "Array & Two Pointers",
        "keywords": ["two sum", "pair sum", "target sum pair", "find pair with sum", "two number sum"],
        "description": "Finds two indices in an array whose elements sum up to a target value in linear O(N) time using a hash map or two pointers.",
        "problem_statement": "Given an array of integers and a target sum, identify the two elements whose sum equals the target."
    },
    {
        "name": "Diffie-Hellman Key Exchange",
        "category": "Cybersecurity & Cryptography",
        "keywords": ["diffie hellman", "diffie-hellman", "key exchange", "asymmetric key agreement", "modular discrete logarithm"],
        "description": "A cryptographic protocol that allows two parties to securely establish a shared secret key over an insecure communication channel.",
        "problem_statement": "Compute a shared secret key across an open network without either party revealing their private exponents."
    },
    {
        "name": "SHA-256 Cryptographic Hash",
        "category": "Cybersecurity & Cryptography",
        "keywords": ["sha-256", "sha256", "sha 256", "sha 256 algorithm", "sha-256 algorithm", "sha256 algorithm", "secure hash algorithm", "cryptographic hash function", "256 bit digest"],
        "description": "A cryptographic hash function designed by NSA that maps arbitrary-length input data to a fixed 256-bit digest with strong collision resistance.",
        "problem_statement": "Produce a unique, deterministic 256-bit irreversible hash digest for any input message."
    },
    {
        "name": "Karatsuba Multiplication",
        "category": "Mathematics",
        "keywords": ["karatsuba", "fast multiplication", "divide and conquer multiplication", "fast integer product"],
        "description": "A divide-and-conquer fast multiplication algorithm that computes the product of two n-digit numbers using 3 recursive multiplications instead of 4 in O(N^1.585) time.",
        "problem_statement": "Multiply two large integers asymptotically faster than traditional O(N^2) grade-school multiplication."
    },
    {
        "name": "Miller-Rabin Primality Test",
        "category": "Mathematics",
        "keywords": ["miller rabin", "miller-rabin", "primality test", "probabilistic prime test", "composite witness"],
        "description": "A randomized, probabilistic primality test that determines whether a given number is composite or probable prime using modular square roots of 1.",
        "problem_statement": "Determine whether an odd integer n is prime with arbitrarily low error probability across k independent witness rounds."
    },
    {
        "name": "Paxos Consensus Algorithm",
        "category": "Distributed Systems",
        "keywords": ["paxos", "paxos consensus", "distributed consensus", "synod protocol", "proposer acceptor learner"],
        "description": "A consensus protocol for reaching agreement on a single data value among a network of unreliable or fault-prone processors.",
        "problem_statement": "Achieve safety and eventual liveness consensus across distributed nodes despite message delays, reorderings, and node crashes."
    },
    {
        "name": "Raft Consensus Algorithm",
        "category": "Distributed Systems",
        "keywords": ["raft", "raft consensus", "leader election log replication", "distributed state machine", "replicated log"],
        "description": "An understandable distributed consensus algorithm that manages a replicated log through explicit leader election, log replication, and safety invariants.",
        "problem_statement": "Maintain a consistent, linearizable replicated state machine log across a cluster of distributed server nodes."
    },
    {
        "name": "LRU Cache Replacement Algorithm",
        "category": "Database & Indexing",
        "keywords": ["lru cache", "lru", "least recently used", "cache eviction", "cache replacement", "page replacement lru"],
        "description": "A cache eviction algorithm that discards the least recently used items first when cache capacity is exceeded, implemented in O(1) time using a Hash Map and Doubly Linked List.",
        "problem_statement": "Maintain a fixed-capacity memory cache supporting O(1) get and put operations while evicting the least recently accessed item on overflow."
    }
]

# Seamlessly integrate Machine Learning, Number Systems, and Encoding algorithms
for item in ML_ENCODING_REGISTRY:
    ALGORITHM_PROMPT_KNOWLEDGE_BASE.append({
        "name": item["algorithm_name"],
        "category": item["category"],
        "keywords": item["keywords"],
        "description": item["description"],
        "problem_statement": item["problem_statement"]
    })

# Explicit Blacklist for Non-Algorithmic Queries (Everyday objects, names, food, greetings)
REJECTED_NON_ALGORITHM_TERMS = {
    # Personal / Family / User Names
    "habeeb", "vignan", "lara", "john", "alice", "bob", "rahul", "smith", "david",
    "michael", "sarah", "emma", "alex", "mohammed", "ahmed", "joseph", "charles",
    "william", "james", "robert", "mary", "patricia", "jennifer", "linda", "elizabeth",
    "suresh", "ramesh", "rajesh", "priya", "anita", "kumar", "singh", "sharma",
    "sravani", "bhavani", "likhith", "likhit", "kiran", "sai", "teja", "vamsi",
    # Colleges, Places, Institutions
    "vignan", "lara", "college", "university", "school", "hospital", "institute",
    "hyderabad", "delhi", "mumbai", "chennai", "bangalore", "london", "paris",
    "new york", "america", "india", "harvard", "stanford", "oxford", "cambridge",
    # Physical objects, vehicles, furniture, household items
    "car", "cars", "bus", "buses", "truck", "trucks", "bike", "bikes", "bicycle",
    "motorcycle", "train", "trains", "plane", "planes", "airplane", "aeroplane",
    "boat", "ship", "chair", "chairs", "table", "tables", "desk", "door", "doors",
    "fan", "fans", "bed", "beds", "sofa", "pillow", "blanket",
    "pen", "pencil", "paper", "book", "books", "bottle", "cup", "glass", "plate",
    "spoon", "fork", "knife", "shirt", "pant", "pants", "tshirt", "shoe", "shoes",
    "sock", "socks", "hat", "cap", "bag", "backpack", "wallet", "watch", "clock",
    "key", "keys", "lock", "mirror", "lamp", "bulb", "box", "house", "room", "wall",
    "floor", "roof", "road", "street",
    # Food, drinks, animals
    "apple", "apples", "banana", "bananas", "mango", "mangoes", "orange", "oranges",
    "grape", "grapes", "lemon", "potato", "tomato", "onion", "pizza", "burger",
    "sandwich", "bread", "rice", "pasta", "chicken", "meat", "egg", "eggs", "water",
    "milk", "tea", "coffee", "juice", "fruit", "fruits", "vegetable", "vegetables",
    "dog", "dogs", "cat", "cats", "cow", "cows", "horse", "sheep", "goat", "pig",
    "lion", "lions", "tiger", "tigers", "elephant", "bear", "monkey", "bird", "birds",
    "duck", "fish", "snake",
    # Greetings, conversational, arbitrary non-algorithms
    "hello", "hi", "hey", "test", "testing", "ok", "okay", "yes", "no", "who", "what",
    "where", "why", "how are you", "good morning", "good afternoon", "good evening",
    "good night", "thanks", "thank you", "bye", "goodbye", "please", "nothing", "anything",
    "something", "whatever", "random", "custom", "magic", "cool", "funny", "smart", "super",
    "mega", "fake", "unknown", "dummy", "sample", "foo", "bar", "baz", "abc", "xyz", "qwerty",
    "asdf", "hjkl", "zxcv"
}

# Noise & Gibberish Patterns
REPEATED_CHAR_REGEX = re.compile(r"(.)\1{4,}")
NON_ALPHANUMERIC_NOISE = re.compile(r"^[^a-zA-Z0-9]+$")

# Common English & CS vocabulary words for validation
COMMON_VOCABULARY = {
    "find", "search", "sort", "algorithm", "path", "shortest", "max", "maximum", "min", "minimum",
    "sum", "array", "graph", "tree", "string", "number", "numbers", "node", "nodes", "edge", "edges",
    "weight", "weighted", "dynamic", "programming", "greedy", "traverse", "traversal", "level",
    "depth", "breadth", "first", "divide", "conquer", "order", "sequence", "element", "elements",
    "calculate", "compute", "give", "me", "show", "generate", "create", "how", "to", "for", "with",
    "in", "of", "an", "a", "the", "using", "by", "value", "values", "capacity", "item", "items",
    "gcd", "lcm", "prime", "primes", "cycle", "detect", "power", "exponentiation", "heap", "stack",
    "queue", "matrix", "coin", "coins", "change", "edit", "distance", "palindrome", "reverse",
    "annealing", "simulated", "swarm", "particle", "pso", "tabu", "pheromone", "colony", "wolf",
    "heuristic", "metaheuristic", "metaheuristics", "crossover", "mutation", "evolution", "fitness",
    "graham", "scan", "jarvis", "march", "simplex", "dantzig", "karatsuba", "strassen", "timsort",
    "needleman", "wunsch", "smith", "waterman", "paxos", "raft", "chandy", "lamport", "bloom",
    "apriori", "page", "rank", "aho", "corasick", "boyer", "moore", "welch", "lempel", "ziv",
    "filter", "decomposition", "elimination", "triangulation", "voronoi", "delaunay", "polygon", "sweep"
}

CS_INDICATORS = {
    "sort", "sorting", "search", "searching", "traversal", "traversals",
    "tree", "trees", "graph", "graphs", "dp", "dynamic", "programming", "greedy",
    "heuristic", "metaheuristic", "genetic", "evolutionary", "annealing", "clustering",
    "regression", "classification", "classifier", "neural", "network", "encoding",
    "compression", "cipher", "crypto", "cryptography", "queue", "stack", "linked",
    "list", "hash", "hashing", "routing", "path", "shortest", "mst", "knapsack",
    "subarray", "subsequence", "distance", "forest", "bayes", "svm", "knn", "pca",
    "kmeans", "dbscan", "qlearning", "rl", "automata", "turing", "automaton", "matrix",
    "divide", "conquer", "backtracking", "branch", "bound", "binary", "octal", "hex",
    "hexadecimal", "base64", "shannon", "huffman", "hamming", "rle", "ols", "sgd",
    "bridge", "bridges", "tarjan", "finding", "bipartite", "matching", "flow", "simplex",
    "fft", "fourier", "manacher", "skip", "skiplist", "convex", "hull", "sieve", "prime",
    "mcts", "minimax", "alpha", "beta", "markov", "viterbi", "policy", "agent", "actor",
    "critic", "swarm", "colony", "treap", "splay", "fenwick", "segment", "trie", "bloom",
    "pagerank", "hopcroft", "karp", "kuhn", "munkres", "hungarian", "euler", "hamilton",
    "boyer", "moore", "shaker", "strassen", "karatsuba", "eratosthenes", "rabin", "cocktail",
    "dijkstra", "kadane", "prim", "prims", "kruskal", "kruskals", "bellman", "floyd", "warshall",
    "optimizer", "method", "reverse", "fibonacci", "factorial", "rsa", "aes", "des",
    "encryption", "decryption", "array", "arrays", "integer", "integers", "string", "strings",
    "ascending", "descending", "inorder", "preorder", "postorder", "levelorder", "level",
    "order", "kmp", "knuth", "morris", "pratt", "lzw", "lempel", "ziv", "welch", "kahn",
    "kahns", "union", "find", "dsu", "disjoint", "set", "pointers", "pointer", "sliding",
    "window", "dutch", "flag", "tortoise", "hare", "coin", "coins", "change", "bst",
    "fulkerson", "dinic", "dinics", "sha", "sha256", "graham", "scan", "jarvis", "march",
    "dantzig", "needleman", "wunsch", "smith", "waterman", "paxos", "raft", "chandy",
    "lamport", "apriori", "filter", "decomposition", "elimination", "triangulation",
    "voronoi", "delaunay", "polygon", "sweep", "timsort", "comb", "gnome", "pancake",
    "bt", "depth", "height", "lca", "ancestor", "diameter", "leaf", "leaves", "root"
}

def validate_input(prompt: str) -> Dict[str, Any]:
    """
    Validates whether the user search query or prompt is a meaningful algorithm request.
    Filters out keyboard smashes, random numbers, non-alphanumeric noise, character repetition,
    and arbitrary non-CS terms combined with 'algorithm'.
    """
    clean_prompt = prompt.strip()

    if not clean_prompt:
        return {
            "is_valid": False,
            "reason": "Please enter an algorithm name or description prompt."
        }

    # Length check (Allow short acronyms like BFS, DFS, MST, LCS, TSP, GCD, LCM)
    if len(clean_prompt) < 2:
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Query is too short. Please enter a valid algorithm name or prompt."
        }

    # Check non-alphanumeric noise
    if NON_ALPHANUMERIC_NOISE.match(clean_prompt):
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Input contains only symbols or punctuation. Please provide a valid query."
        }

    # Check repeated characters (e.g. "aaaaaaa", "zzzzzzz")
    if REPEATED_CHAR_REGEX.search(clean_prompt.lower()):
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Unnatural character repetition detected. Please provide a meaningful query."
        }

    prompt_lower = clean_prompt.lower()
    words = [w for w in re.findall(r"[a-z0-9]+", prompt_lower)]

    if not words:
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Could not detect readable terms in input query."
        }

    # Check typical QWERTY smash patterns and noise across all words
    smash_patterns = ["asdf", "qwerty", "zxcv", "hjkl", "12345", "98765"]
    for w in words:
        if any(sp in w for sp in smash_patterns):
            return {
                "is_valid": False,
                "reason": "Invalid prompt: Could not understand user prompt. Please provide a valid algorithm query."
            }

    stop_words_set = {"in", "for", "to", "a", "an", "the", "of", "with", "using", "how", "give", "me", "show", "what", "is", "and", "algorithm", "algorithms", "problem", "problems", "solve", "code", "implement", "write", "generate", "create"}
    meaningful_words = [w for w in words if w not in stop_words_set]

    if not meaningful_words:
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Please enter a specific computer science algorithm name or problem prompt."
        }

    # If it's a single word, verify it is not a random consonant smash
    if len(words) == 1:
        single_word = words[0]
        # Acronyms or valid short terms
        valid_acronyms = {"bfs", "dfs", "mst", "lcs", "lis", "tsp", "dp", "sort", "search", "tree", "graph", "gcd", "lcm", "kmp", "pso", "sa", "ga", "aco", "gwo", "de", "ts", "rsa", "aes", "fft", "lzw", "bst", "dsu", "sha", "mcm"}
        if single_word in valid_acronyms:
            return {"is_valid": True}

        # Keyboard smash heuristic: if single word has no vowels and length >= 4
        vowels = set("aeiouy")
        has_vowels = any(c in vowels for c in single_word)
        if not has_vowels and len(single_word) >= 4:
            return {
                "is_valid": False,
                "reason": "Invalid prompt: Could not understand user prompt. Please enter a valid algorithm name or description."
            }

    # Verify query contains at least one alphabetic letter
    if not any(c.isalpha() for c in clean_prompt):
        return {
            "is_valid": False,
            "reason": "Invalid prompt: Query must contain valid alphabetical characters."
        }

    # Multi-word gibberish and keyboard smash heuristic
    for w in words:
        if len(w) >= 4:
            vowels = sum(1 for c in w if c in "aeiouy")
            if vowels == 0:
                return {
                    "is_valid": False,
                    "reason": f"Invalid query '{clean_prompt}': Unrecognized term or keyboard smash. Please search for a valid algorithm name."
                }

    # Strict check: Reject queries matching everyday objects, personal names, food, greetings, or blacklisted non-algorithm terms
    if prompt_lower in REJECTED_NON_ALGORITHM_TERMS or any(w in REJECTED_NON_ALGORITHM_TERMS for w in meaningful_words):
        return {
            "is_valid": False,
            "reason": f"'{clean_prompt}' is not a recognized computer science algorithm. Please search for a defined algorithm (e.g., Dijkstra, Merge Sort, Kadane's, A* Search, Binary Search, etc.)."
        }

    has_cs_indicator = any(w in CS_INDICATORS for w in meaningful_words) or any(ind in prompt_lower for ind in ["encoding", "conversion", "sort", "search", "tree", "graph", "clustering", "regression"])

    if not has_cs_indicator:
        return {
            "is_valid": False,
            "reason": f"'{clean_prompt}' is not a recognized computer science algorithm. Please search for a defined algorithm (e.g., Dijkstra, Merge Sort, Kadane's, A* Search, Binary Search, etc.)."
        }

    return {"is_valid": True}


def extract_intent_domain(prompt: str) -> str:
    """Extracts CS problem domain from natural language prompt."""
    p_lower = prompt.lower()
    if any(k in p_lower for k in ["octal", "binary", "hex", "hexadecimal", "base64", "bcd", "gray code", "manchester", "encoding", "conversion"]):
        return "Number Systems & Encoding"
    if any(k in p_lower for k in ["random forest", "decision tree", "regression", "logistic", "svm", "knn", "naive bayes", "gradient descent", "boosting", "xgboost", "pca", "dbscan", "cluster", "classifier"]):
        return "Machine Learning"
    if any(k in p_lower for k in ["q-learning", "dqn", "sarsa", "reinforcement", "policy gradient", "actor critic"]):
        return "Reinforcement Learning"
    if any(k in p_lower for k in ["compression", "rle", "run length", "lzw", "shannon fano", "huffman", "hamming"]):
        return "Data Compression & Encoding" 
    if any(k in p_lower for k in ["healthcare", "medical", "clinical", "patient", "hospital", "triage", "biomedical", "disease"]):
        return "Healthcare & Biomedical CS"
    if any(k in p_lower for k in ["finance", "financial", "trading", "stock", "portfolio", "sharpe", "black scholes", "markowitz"]):
        return "Finance & Algorithmic Trading"
    if any(k in p_lower for k in ["robotics", "robot", "drone", "autonomous", "slam", "rrt", "motion planning"]):
        return "Robotics & Autonomous Systems"
    if any(k in p_lower for k in ["security", "crypto", "cryptography", "encryption", "rsa", "aes", "cipher"]):
        return "Cybersecurity & Cryptography"
    if any(k in p_lower for k in ["recommendation", "recommender", "collaborative filtering", "matrix factorization"]):
        return "Recommendation Systems"
    if any(k in p_lower for k in ["image processing", "computer vision", "vision", "canny edge", "sobel"]):
        return "Computer Vision & Image Processing"
    if any(k in p_lower for k in ["puzzle", "n-queens", "sudoku", "constraint", "8-puzzle", "sliding puzzle", "tsp", "salesman", "salesperson", "backtrack"]):
        return "Puzzle & Constraint Satisfaction"
    if any(k in p_lower for k in ["database", "db", "b-tree", "btree", "b+ tree", "hash index", "indexing", "lsm"]):
        return "Database & Indexing"
    if any(k in p_lower for k in ["zeroes", "zeros", "two pointer", "sliding window", "move zeroes", "rotate array", "in-place", "partition array", "dutch national"]):
        return "Array & Two Pointers"
    if any(k in p_lower for k in ["metaheuristic", "annealing", "simulated annealing", "particle swarm", "pso", "tabu", "ant colony", "aco", "grey wolf", "gwo", "differential evolution", "evolutionary"]):
        return "Metaheuristic & Evolutionary Algorithms"
    if any(k in p_lower for k in ["sort", "sorting", "order", "arrange"]):
        return "Sorting"
    if any(k in p_lower for k in ["shortest path", "dijkstra", "bellman", "floyd", "graph", "bfs", "dfs", "node", "edge", "routing", "grid", "pathfinding", "mst", "kruskal", "prim", "cycle"]):
        return "Graph Algorithms"
    if any(k in p_lower for k in ["knapsack", "subsequence", "lcs", "lis", "edit distance", "levenshtein", "dynamic programming", "dp", "coin change", "memoization"]):
        return "Dynamic Programming"
    if any(k in p_lower for k in ["binary search", "linear search", "sequential search", "array search", "lookup", "locate"]):
        return "Searching"
    if any(k in p_lower for k in ["compress", "huffman", "string", "pattern", "matching", "kmp", "rabin", "text"]):
        return "String Matching"
    if any(k in p_lower for k in ["gcd", "lcm", "prime", "sieve", "exponentiation", "math", "factorial", "fibonacci", "power"]):
        return "Mathematics"
    return "General"


def parse_user_prompt(prompt: str) -> Dict[str, Any]:
    """
    Parses a user input prompt or algorithm name to understand the intent,
    identify the optimal target algorithm, and extract relevant domain metadata.
    """
    val_res = validate_input(prompt)
    if not val_res["is_valid"]:
        return {
            "is_valid": False,
            "reason": val_res["reason"],
            "raw_prompt": prompt
        }

    clean_prompt = prompt.strip()
    prompt_lower = clean_prompt.lower()
    raw_prompt_words = set(re.findall(r"[a-z0-9]+", prompt_lower))
    stop_words_set = {"in", "for", "to", "a", "an", "the", "of", "with", "using", "find", "algorithm", "algorithms", "write", "generate", "create", "how", "give", "me", "show"}
    meaningful_prompt_words = raw_prompt_words - stop_words_set

    best_match = None
    max_score = 0

    # Match user query against Knowledge Base using word-level and phrase-level scoring
    for item in ALGORITHM_PROMPT_KNOWLEDGE_BASE:
        score = 0
        name_lower = item["name"].lower()
        clean_name = re.sub(r"\s*\([^)]*\)", "", name_lower).strip()
        
        # Exact algorithm name match (including clean name without parentheses)
        if prompt_lower == name_lower or prompt_lower == clean_name:
            score += 120
        elif name_lower in prompt_lower or clean_name in prompt_lower:
            score += 80
        elif prompt_lower in name_lower or prompt_lower in clean_name:
            score += 75

        # Keyword / pattern matching
        for kw in item["keywords"]:
            kw_lower = kw.lower()
            if kw_lower == prompt_lower:
                score += 90
            elif kw_lower in prompt_lower:
                score += 60
            else:
                kw_words = set(re.findall(r"[a-z0-9]+", kw_lower))
                kw_meaningful = kw_words - stop_words_set
                if kw_meaningful and kw_meaningful.issubset(meaningful_prompt_words):
                    score += 50
                elif kw_meaningful:
                    overlap = len(kw_meaningful.intersection(meaningful_prompt_words))
                    if overlap >= 2:
                        score += 30 + (overlap * 5)

        if score > max_score:
            max_score = score
            best_match = item

    if best_match and max_score >= 60:
        is_prompt = (clean_prompt.lower() != best_match["name"].lower())
        return {
            "is_valid": True,
            "raw_prompt": clean_prompt,
            "matched_algorithm": best_match["name"],
            "category": best_match["category"],
            "description_intro": f"Optimal algorithm identified for prompt '{clean_prompt}': {best_match['name']}.",
            "problem_statement": best_match["problem_statement"],
            "is_prompt": is_prompt,
            "confidence": min(1.0, round(max_score / 100.0, 2)),
            "extracted_domain": best_match["category"]
        }

    # Secondary check: Normalized alphanumeric match against defined knowledge base algorithms
    clean_alnum = re.sub(r"[^a-z0-9]", "", prompt_lower)
    if clean_alnum and len(clean_alnum) >= 3:
        for item in ALGORITHM_PROMPT_KNOWLEDGE_BASE:
            item_alnum = re.sub(r"[^a-z0-9]", "", item["name"].lower())
            if clean_alnum == item_alnum or (len(clean_alnum) >= 5 and item_alnum == clean_alnum):
                return {
                    "is_valid": True,
                    "raw_prompt": clean_prompt,
                    "matched_algorithm": item["name"],
                    "category": item["category"],
                    "description_intro": f"Optimal defined algorithm identified for prompt '{clean_prompt}': {item['name']}.",
                    "problem_statement": item["problem_statement"],
                    "is_prompt": True,
                    "confidence": 0.85,
                    "extracted_domain": item["category"]
                }
            for kw in item["keywords"]:
                kw_alnum = re.sub(r"[^a-z0-9]", "", kw.lower())
                if clean_alnum == kw_alnum:
                    return {
                        "is_valid": True,
                        "raw_prompt": clean_prompt,
                        "matched_algorithm": item["name"],
                        "category": item["category"],
                        "description_intro": f"Optimal defined algorithm identified for prompt '{clean_prompt}': {item['name']}.",
                        "problem_statement": item["problem_statement"],
                        "is_prompt": True,
                        "confidence": 0.80,
                        "extracted_domain": item["category"]
                    }

    # Third check: Comprehensive Catalog Check
    from app.services.algorithm_comprehensive_catalog import get_comprehensive_algorithm
    comp = get_comprehensive_algorithm(clean_prompt)
    if comp:
        return {
            "is_valid": True,
            "raw_prompt": clean_prompt,
            "matched_algorithm": comp["name"],
            "category": comp["category"],
            "description_intro": f"Optimal algorithm identified: {comp['name']}.",
            "problem_statement": f"Execute optimal computation for {comp['name']}.",
            "is_prompt": False,
            "confidence": 0.95,
            "extracted_domain": comp["category"]
        }

    # Fourth check: If OpenAI API is available, verify if this is an established CS algorithm
    try:
        from app.services.ai_generator import verify_algorithm_with_openai
        ai_verif = verify_algorithm_with_openai(clean_prompt)
        if ai_verif and ai_verif.get("is_defined"):
            standard_name = ai_verif.get("standard_name", clean_prompt.title())
            category = ai_verif.get("category", "General")
            return {
                "is_valid": True,
                "raw_prompt": clean_prompt,
                "matched_algorithm": standard_name,
                "category": category,
                "description_intro": f"Verified defined algorithm: {standard_name}.",
                "problem_statement": f"Execute standard algorithm solution for {standard_name}.",
                "is_prompt": True,
                "confidence": 0.90,
                "extracted_domain": category
            }
    except Exception:
        pass

    # Fifth check: Valid algorithmic / computational intent verification (excluding generic 'algorithm' / 'problem' / 'solve')
    cs_keywords = CS_INDICATORS
    
    words_in_prompt = set(re.findall(r"[a-z0-9]+", prompt_lower))
    has_recognized_cs_intent = bool(words_in_prompt.intersection(cs_keywords))

    if has_recognized_cs_intent and len(meaningful_prompt_words) >= 1:
        # Check if prompt contains any rejected or non-CS terms
        if any(w in REJECTED_NON_ALGORITHM_TERMS for w in meaningful_prompt_words):
            return {
                "is_valid": False,
                "reason": f"'{clean_prompt}' is not a recognized computer science algorithm. Please search for a defined algorithm (e.g., Dijkstra, Merge Sort, Kadane's, A* Search, Binary Search, etc.).",
                "raw_prompt": clean_prompt
            }

        # Check if any word in meaningful_prompt_words is unknown / non-CS
        invalid_words = [w for w in meaningful_prompt_words if w not in cs_keywords and w not in CS_INDICATORS and w not in COMMON_VOCABULARY]
        if invalid_words:
            return {
                "is_valid": False,
                "reason": f"'{clean_prompt}' is not a recognized computer science algorithm. Please search for a defined algorithm (e.g., Dijkstra, Merge Sort, Kadane's, A* Search, Binary Search, etc.).",
                "raw_prompt": clean_prompt
            }

        inferred_domain = extract_intent_domain(clean_prompt)
        if inferred_domain == "General":
            inferred_domain = "Computer Science Algorithms"

        # Format clean algorithm name
        clean_name = re.sub(r"^(how to implement|implement|write|generate|create|find|give me|solve|show|explain|code for)\s+", "", clean_prompt, flags=re.IGNORECASE).strip()
        words = clean_name.split()
        capitalized_words = [w.capitalize() for w in words]
        formatted_name = " ".join(capitalized_words)

        if not formatted_name.lower().endswith("algorithm") and not any(k in formatted_name.lower() for k in ["sort", "search", "tree", "problem", "optimizer", "method", "network", "scan", "filter", "elimination", "decomposition", "traversal", "solver", "heuristic", "sieve", "multiplication", "transform", "fft"]):
            formatted_name = f"{formatted_name} Algorithm"

        return {
            "is_valid": True,
            "raw_prompt": clean_prompt,
            "matched_algorithm": formatted_name,
            "category": inferred_domain,
            "description_intro": f"Computational algorithm synthesized for '{clean_prompt}': {formatted_name}.",
            "problem_statement": f"Execute optimal algorithmic computation for {formatted_name}.",
            "is_prompt": True,
            "confidence": 0.82,
            "extracted_domain": inferred_domain
        }

    # REJECT ALL UNRECOGNIZED GIBBERISH / NON-ALGORITHMIC INPUTS
    return {
        "is_valid": False,
        "reason": f"No recognized computer science algorithm or computational problem found for '{clean_prompt}'. Please enter a valid algorithm name (e.g., 'Dijkstra', 'Kadane', 'Binary Search', 'QuickSort', 'A* Search', '0/1 Knapsack').",
        "raw_prompt": clean_prompt
    }


