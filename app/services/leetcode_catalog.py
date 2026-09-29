"""
LeetCode Problem Catalog & Recommendation Engine
Maps computer science algorithms and problem queries to curated LeetCode problems
with direct URLs, difficulty ratings, topic tags, descriptions, sample I/O, and solving tips.
"""

from typing import List, Dict, Any, Optional
import re

# Comprehensive curated LeetCode catalog mapped by canonical algorithm keys
LEETCODE_DATABASE: Dict[str, List[Dict[str, Any]]] = {
    "palindrome": [
        {
            "id": 5,
            "title": "Longest Palindromic Substring",
            "slug": "longest-palindromic-substring",
            "url": "https://leetcode.com/problems/longest-palindromic-substring/",
            "difficulty": "Medium",
            "acceptance_rate": "33.8%",
            "topic_tags": ["Two Pointers", "String", "Dynamic Programming", "Manacher's Algorithm"],
            "description": "Given a string s, return the longest palindromic substring in s. Solvable in linear O(N) time using Manacher's Algorithm.",
            "relevance": "Direct implementation of Manacher's Algorithm expanding around palindrome radiuses using boundary symmetry.",
            "sample_io": "Input: s = 'babad' | Output: 'bab'",
            "approach_tip": "Transform string with delimiters (e.g. '^#a#b#a#$') to treat even and odd palindromes uniformly. Maintain center C and right edge R."
        },
        {
            "id": 647,
            "title": "Palindromic Substrings",
            "slug": "palindromic-substrings",
            "url": "https://leetcode.com/problems/palindromic-substrings/",
            "difficulty": "Medium",
            "acceptance_rate": "69.1%",
            "topic_tags": ["Two Pointers", "String", "Dynamic Programming"],
            "description": "Given a string s, return the number of palindromic substrings in it.",
            "relevance": "Count palindrome radius lengths directly derived from the Manacher radius array P[i].",
            "sample_io": "Input: s = 'aaa' | Output: 6",
            "approach_tip": "Each radius length r contributes (r // 2) palindromes. Sum over all positions in linear time."
        },
        {
            "id": 214,
            "title": "Shortest Palindrome",
            "slug": "shortest-palindrome",
            "url": "https://leetcode.com/problems/shortest-palindrome/",
            "difficulty": "Hard",
            "acceptance_rate": "34.5%",
            "topic_tags": ["String", "Rolling Hash", "String Matching"],
            "description": "Find the shortest palindrome you can build by adding characters in front of string s.",
            "relevance": "Advanced string palindrome computation solvable via KMP prefix function or Manacher's radius tracking.",
            "sample_io": "Input: s = 'aacecaaa' | Output: 'aaacecaaa'",
            "approach_tip": "Find longest palindromic prefix of s, then prepend reversed suffix."
        }
    ],

    "skiplist": [
        {
            "id": 1206,
            "title": "Design Skiplist",
            "slug": "design-skiplist",
            "url": "https://leetcode.com/problems/design-skiplist/",
            "difficulty": "Hard",
            "acceptance_rate": "54.7%",
            "topic_tags": ["Linked List", "Design"],
            "description": "Design a Skiplist without using any built-in libraries. Implement search, add, and erase in O(log n) expected time.",
            "relevance": "Exact textbook problem: design a multi-level probabilistic Skip List with coin-flip tower promotion.",
            "sample_io": 'Input: ["Skiplist", "add", "add", "search", "erase"] | Output: [null, null, null, true, true]',
            "approach_tip": "Use a Node with forward pointers array of size MAX_LEVEL. Maintain predecessors array on each search."
        },
        {
            "id": 707,
            "title": "Design Linked List",
            "slug": "design-linked-list",
            "url": "https://leetcode.com/problems/design-linked-list/",
            "difficulty": "Medium",
            "acceptance_rate": "27.9%",
            "topic_tags": ["Linked List", "Design"],
            "description": "Design your implementation of the linked list supporting indexed operations in O(1) to O(N) time.",
            "relevance": "Core linked structure manipulation prerequisite to Skip List multi-level pointers.",
            "sample_io": 'Input: ["MyLinkedList", "addAtHead", "addAtTail"] | Output: [null, null, null]',
            "approach_tip": "Maintain head and tail sentinel dummy nodes to simplify pointer re-wiring."
        }
    ],

    "graph_bridges": [
        {
            "id": 1192,
            "title": "Critical Connections in a Network",
            "slug": "critical-connections-in-a-network",
            "url": "https://leetcode.com/problems/critical-connections-in-a-network/",
            "difficulty": "Hard",
            "acceptance_rate": "55.8%",
            "topic_tags": ["Depth-First Search", "Graph", "Biconnected Component"],
            "description": "Find all critical connections in a network whose removal causes some servers to be unable to reach each other.",
            "relevance": "Textbook implementation of Tarjan's Bridge-Finding algorithm using low-link values low[v] > rank[u].",
            "sample_io": "Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]] | Output: [[1,3]]",
            "approach_tip": "Maintain rank/discovery array and low array. Edge (u, v) is a bridge if low[v] > rank[u]."
        },
        {
            "id": 802,
            "title": "Find Eventual Safe States",
            "slug": "find-eventual-safe-states",
            "url": "https://leetcode.com/problems/find-eventual-safe-states/",
            "difficulty": "Medium",
            "acceptance_rate": "62.5%",
            "topic_tags": ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"],
            "description": "Return an array of all safe nodes in directed graph that only lead to terminal nodes.",
            "relevance": "Cycle detection in directed graphs related to Tarjan's SCC and topological sorting.",
            "sample_io": "Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]] | Output: [2,4,5,6]",
            "approach_tip": "Use 3-color DFS (0=unvisited, 1=visiting, 2=safe) or reverse edges and Kahn's algorithm."
        }
    ],

    "bipartite_matching": [
        {
            "id": 785,
            "title": "Is Graph Bipartite?",
            "slug": "is-graph-bipartite",
            "url": "https://leetcode.com/problems/is-graph-bipartite/",
            "difficulty": "Medium",
            "acceptance_rate": "55.4%",
            "topic_tags": ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"],
            "description": "Given an undirected graph, return true if and only if it is bipartite.",
            "relevance": "Fundamental prerequisite check for Hopcroft-Karp and Hungarian bipartite algorithms.",
            "sample_io": "Input: graph = [[1,2,3],[0,2],[0,1,3],[0,2]] | Output: false",
            "approach_tip": "2-color BFS or DFS: assign alternating colors {0, 1} to neighbors; fail if neighbor has identical color."
        },
        {
            "id": 1820,
            "title": "Maximum Number of Accepted Invitations",
            "slug": "maximum-number-of-accepted-invitations",
            "url": "https://leetcode.com/problems/maximum-number-of-accepted-invitations/",
            "difficulty": "Medium",
            "acceptance_rate": "56.2%",
            "topic_tags": ["Array", "Graph", "Maximum Flow", "Bipartite Matching"],
            "description": "Find the maximum number of accepted party invitations between boys and girls.",
            "relevance": "Direct Maximum Cardinality Bipartite Matching solved via Hopcroft-Karp or Hungarian method.",
            "sample_io": "Input: grid = [[1,1,1],[1,0,1],[0,0,1]] | Output: 3",
            "approach_tip": "Find augmenting paths using DFS/BFS; update matches and alternate paths until no augmenting path remains."
        }
    ],

    "fast_fourier_transform": [
        {
            "id": 43,
            "title": "Multiply Strings",
            "slug": "multiply-strings",
            "url": "https://leetcode.com/problems/multiply-strings/",
            "difficulty": "Medium",
            "acceptance_rate": "40.8%",
            "topic_tags": ["Math", "String", "Simulation"],
            "description": "Given two non-negative integers represented as strings, return their product. Solvable asymptotically via FFT / Karatsuba.",
            "relevance": "Fast polynomial and large number multiplication benchmark for Cooley-Tukey FFT and Karatsuba algorithms.",
            "sample_io": "Input: num1 = '123', num2 = '456' | Output: '56088'",
            "approach_tip": "Treat numbers as coefficients of polynomials A(x) and B(x); evaluate via FFT, point-multiply, and interpolate."
        },
        {
            "id": 50,
            "title": "Pow(x, n)",
            "slug": "powx-n",
            "url": "https://leetcode.com/problems/powx-n/",
            "difficulty": "Medium",
            "acceptance_rate": "35.4%",
            "topic_tags": ["Math", "Recursion"],
            "description": "Implement pow(x, n), which calculates x raised to the power n in O(log n) time.",
            "relevance": "Binary exponentiation divide-and-conquer strategy mirroring FFT twiddle factor radix evaluation.",
            "sample_io": "Input: x = 2.00000, n = 10 | Output: 1024.00000",
            "approach_tip": "x^n = (x^(n/2))^2 if n is even, else x * (x^(n/2))^2."
        }
    ],

    "dijkstra": [
        {
            "id": 743,
            "title": "Network Delay Time",
            "slug": "network-delay-time",
            "url": "https://leetcode.com/problems/network-delay-time/",
            "difficulty": "Medium",
            "acceptance_rate": "54.2%",
            "topic_tags": ["Graph", "Shortest Path", "Heap (Priority Queue)", "Breadth-First Search"],
            "description": "You are given a network of n nodes labeled from 1 to n, and times list of directed edges times[i] = (u, v, w). Determine the minimum time required for a signal sent from node k to reach all nodes.",
            "relevance": "Direct canonical application of Dijkstra's single-source shortest path algorithm on a weighted directed graph using a min-heap.",
            "sample_io": "Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 | Output: 2",
            "approach_tip": "Maintain a min-heap of (cumulative_distance, node). Pop the lowest cost node, skip if already visited with lower cost, relax outgoing neighbors."
        },
        {
            "id": 787,
            "title": "Cheapest Flights Within K Stops",
            "slug": "cheapest-flights-within-k-stops",
            "url": "https://leetcode.com/problems/cheapest-flights-within-k-stops/",
            "difficulty": "Medium",
            "acceptance_rate": "39.4%",
            "topic_tags": ["Graph", "Shortest Path", "Dynamic Programming", "Heap"],
            "description": "Find the cheapest price from source to destination city with at most k stops among n cities and given flight prices.",
            "relevance": "Modified Dijkstra or Bellman-Ford tracking state (cost, city, stops) to find shortest path under hop constraints.",
            "sample_io": "Input: n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1 | Output: 700",
            "approach_tip": "Track minimum stops required to reach each node to avoid cycle traps while relaxing edges."
        },
        {
            "id": 1631,
            "title": "Path With Minimum Effort",
            "slug": "path-with-minimum-effort",
            "url": "https://leetcode.com/problems/path-with-minimum-effort/",
            "difficulty": "Medium",
            "acceptance_rate": "59.8%",
            "topic_tags": ["Array", "Binary Search", "Graph", "Heap", "Union Find"],
            "description": "Find a route from top-left to bottom-right of a 2D grid that minimizes the maximum absolute difference in heights between two consecutive cells.",
            "relevance": "Minimax shortest path solvable by Dijkstra's algorithm where edge weight is max height difference encountered.",
            "sample_io": "Input: heights = [[1,2,2],[3,8,2],[5,3,5]] | Output: 2",
            "approach_tip": "Use Dijkstra where the metric relaxed at each step is max(current_effort, abs(height_diff))."
        },
        {
            "id": 1514,
            "title": "Path with Maximum Probability",
            "slug": "path-with-maximum-probability",
            "url": "https://leetcode.com/problems/path-with-maximum-probability/",
            "difficulty": "Medium",
            "acceptance_rate": "57.5%",
            "topic_tags": ["Graph", "Shortest Path", "Heap (Priority Queue)"],
            "description": "Given an undirected weighted graph with probabilities of success, find the path with maximum probability from start to end.",
            "relevance": "Dijkstra adapted with a max-heap multiplying probabilities instead of adding additive costs.",
            "sample_io": "Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2 | Output: 0.25000",
            "approach_tip": "Use a max-heap (or negative log probabilities with min-heap) to select nodes with highest reachable probability first."
        }
    ],

    "bellman_ford": [
        {
            "id": 787,
            "title": "Cheapest Flights Within K Stops",
            "slug": "cheapest-flights-within-k-stops",
            "url": "https://leetcode.com/problems/cheapest-flights-within-k-stops/",
            "difficulty": "Medium",
            "acceptance_rate": "39.4%",
            "topic_tags": ["Dynamic Programming", "Shortest Path", "Graph"],
            "description": "Find the cheapest price from src to dst with at most k stops.",
            "relevance": "Bellman-Ford algorithm executed exactly k+1 iterations to handle edges with hop limits.",
            "sample_io": "Input: n = 4, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, k = 1 | Output: 200",
            "approach_tip": "Run k+1 edge relaxations copying distances array each iteration to prevent cascading within the same step."
        },
        {
            "id": 743,
            "title": "Network Delay Time",
            "slug": "network-delay-time",
            "url": "https://leetcode.com/problems/network-delay-time/",
            "difficulty": "Medium",
            "acceptance_rate": "54.2%",
            "topic_tags": ["Graph", "Shortest Path"],
            "description": "Calculate minimum time for signal to reach all nodes in a network.",
            "relevance": "Can be solved using standard V-1 passes of Bellman-Ford edge relaxation.",
            "sample_io": "Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 | Output: 2",
            "approach_tip": "Iterate n-1 times over all edges, updating dist[v] = min(dist[v], dist[u] + w)."
        }
    ],

    "floyd_warshall": [
        {
            "id": 1334,
            "title": "Find the City With the Smallest Number of Neighbors at a Threshold Distance",
            "slug": "find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance",
            "url": "https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/",
            "difficulty": "Medium",
            "acceptance_rate": "62.3%",
            "topic_tags": ["Dynamic Programming", "Graph", "Shortest Path"],
            "description": "Given n cities and weighted edges, return the city that can reach the smallest number of cities within distanceThreshold.",
            "relevance": "Textbook all-pairs shortest path problem solvable via Floyd-Warshall O(N^3) DP.",
            "sample_io": "Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4 | Output: 3",
            "approach_tip": "Initialize an N x N matrix with edge weights, then triple nested loop over intermediate nodes k, source i, dest j."
        },
        {
            "id": 2976,
            "title": "Minimum Cost to Convert String I",
            "slug": "minimum-cost-to-convert-string-i",
            "url": "https://leetcode.com/problems/minimum-cost-to-convert-string-i/",
            "difficulty": "Medium",
            "acceptance_rate": "53.6%",
            "topic_tags": ["Array", "String", "Graph", "Shortest Path"],
            "description": "Find the minimum cost to convert string source to target by transforming characters using a set of transformation costs.",
            "relevance": "Run Floyd-Warshall on the 26 lowercase character graph (26^3 steps) to compute minimum conversion cost between every letter pair.",
            "sample_io": "Input: source = 'abcd', target = 'acbe', original = ['a','b','c','c','e','d'], changed = ['b','c','b','e','b','e'], cost = [2,5,5,1,2,20] | Output: 28",
            "approach_tip": "Build 26x26 adjacency matrix. Run Floyd-Warshall once, then sum lookup costs for each character."
        }
    ],

    "binary_search": [
        {
            "id": 704,
            "title": "Binary Search",
            "slug": "binary-search",
            "url": "https://leetcode.com/problems/binary-search/",
            "difficulty": "Easy",
            "acceptance_rate": "57.8%",
            "topic_tags": ["Array", "Binary Search"],
            "description": "Given an array of integers nums sorted in ascending order and an integer target, search for target in nums. Return its index or -1.",
            "relevance": "The fundamental classic Binary Search algorithm operating in O(log N) logarithmic time.",
            "sample_io": "Input: nums = [-1,0,3,5,9,12], target = 9 | Output: 4",
            "approach_tip": "Maintain left and right pointers. Calculate mid = left + (right - left) // 2 to avoid integer overflow."
        },
        {
            "id": 33,
            "title": "Search in Rotated Sorted Array",
            "slug": "search-in-rotated-sorted-array",
            "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
            "difficulty": "Medium",
            "acceptance_rate": "40.9%",
            "topic_tags": ["Array", "Binary Search"],
            "description": "Given an integer array nums sorted in ascending order that is possibly rotated at an unknown pivot index, find the index of target in O(log n).",
            "relevance": "Advanced binary search testing condition branching when one half of the search partition is always strictly sorted.",
            "sample_io": "Input: nums = [4,5,6,7,0,1,2], target = 0 | Output: 4",
            "approach_tip": "Determine whether the left half or right half is sorted, then check if target falls inside that sorted range."
        },
        {
            "id": 875,
            "title": "Koko Eating Bananas",
            "slug": "koko-eating-bananas",
            "url": "https://leetcode.com/problems/koko-eating-bananas/",
            "difficulty": "Medium",
            "acceptance_rate": "50.1%",
            "topic_tags": ["Array", "Binary Search"],
            "description": "Return the minimum integer eating speed k such that Koko can eat all piles of bananas within h hours.",
            "relevance": "Binary search on monotonic answer space [1, max(piles)] to find minimum feasible threshold.",
            "sample_io": "Input: piles = [3,6,7,11], h = 8 | Output: 4",
            "approach_tip": "Binary search the speed k. For each k, sum ceil(pile / k). If total hours <= h, search left; else search right."
        },
        {
            "id": 4,
            "title": "Median of Two Sorted Arrays",
            "slug": "median-of-two-sorted-arrays",
            "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/",
            "difficulty": "Hard",
            "acceptance_rate": "41.2%",
            "topic_tags": ["Array", "Binary Search", "Divide and Conquer"],
            "description": "Given two sorted arrays nums1 and nums2 of size m and n, return the median of the two sorted arrays in O(log (m+n)) runtime.",
            "relevance": "Masterclass divide-and-conquer binary search partitioning both arrays simultaneously.",
            "sample_io": "Input: nums1 = [1,3], nums2 = [2] | Output: 2.00000",
            "approach_tip": "Binary search partition index on the smaller array such that max(left) <= min(right) across both partitions."
        }
    ],

    "merge_sort": [
        {
            "id": 912,
            "title": "Sort an Array",
            "slug": "sort-an-array",
            "url": "https://leetcode.com/problems/sort-an-array/",
            "difficulty": "Medium",
            "acceptance_rate": "58.4%",
            "topic_tags": ["Array", "Divide and Conquer", "Sorting", "Merge Sort"],
            "description": "Given an array of integers nums, sort the array in ascending order in O(n log(n)) time and with the smallest space complexity possible.",
            "relevance": "Direct implementation of Merge Sort divide-and-conquer strategy guaranteeing stable O(N log N) performance.",
            "sample_io": "Input: nums = [5,2,3,1] | Output: [1,2,3,5]",
            "approach_tip": "Recursively split the array at mid, sort both halves, and merge the two sorted halves using two pointers."
        },
        {
            "id": 148,
            "title": "Sort List",
            "slug": "sort-list",
            "url": "https://leetcode.com/problems/sort-list/",
            "difficulty": "Medium",
            "acceptance_rate": "58.0%",
            "topic_tags": ["Linked List", "Two Pointers", "Divide and Conquer", "Sorting", "Merge Sort"],
            "description": "Given the head of a linked list, return the list after sorting it in ascending order in O(n log n) time and O(1) memory.",
            "relevance": "Bottom-up or top-down Merge Sort implemented on singly linked lists with O(1) auxiliary space.",
            "sample_io": "Input: head = [4,2,1,3] | Output: [1,2,3,4]",
            "approach_tip": "Use slow/fast pointer to find middle node, split list into two, recurse, then merge two sorted linked lists."
        },
        {
            "id": 493,
            "title": "Reverse Pairs",
            "slug": "reverse-pairs",
            "url": "https://leetcode.com/problems/reverse-pairs/",
            "difficulty": "Hard",
            "acceptance_rate": "31.0%",
            "topic_tags": ["Array", "Binary Search", "Divide and Conquer", "Binary Indexed Tree", "Merge Sort"],
            "description": "Given an integer array nums, return the number of reverse pairs (i, j) where i < j and nums[i] > 2 * nums[j].",
            "relevance": "Piggybacks on Merge Sort's combine step to count inversion-style constraints in O(N log N).",
            "sample_io": "Input: nums = [1,3,2,3,1] | Output: 2",
            "approach_tip": "During the merge step between left and right sorted subarrays, count pairs where left[i] > 2 * right[j] before merging."
        }
    ],

    "quick_sort": [
        {
            "id": 215,
            "title": "Kth Largest Element in an Array",
            "slug": "kth-largest-element-in-an-array",
            "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
            "difficulty": "Medium",
            "acceptance_rate": "67.1%",
            "topic_tags": ["Array", "Divide and Conquer", "Sorting", "Heap", "Quickselect"],
            "description": "Given an integer array nums and an integer k, return the kth largest element in the array without full sorting.",
            "relevance": "Textbook application of Quickselect (Hoare's selection algorithm derived from Quick Sort partition) running in average O(N) time.",
            "sample_io": "Input: nums = [3,2,1,5,6,4], k = 2 | Output: 5",
            "approach_tip": "Choose a random pivot, partition array into elements greater, equal, and smaller than pivot. Recurse only into the target partition."
        },
        {
            "id": 75,
            "title": "Sort Colors",
            "slug": "sort-colors",
            "url": "https://leetcode.com/problems/sort-colors/",
            "difficulty": "Medium",
            "acceptance_rate": "63.5%",
            "topic_tags": ["Array", "Two Pointers", "Sorting"],
            "description": "Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent.",
            "relevance": "Dutch National Flag 3-way partitioning algorithm used in 3-way Quick Sort to handle duplicate keys.",
            "sample_io": "Input: nums = [2,0,2,1,1,0] | Output: [0,0,1,1,2,2]",
            "approach_tip": "Maintain three pointers: low, mid, high. Swap 0s to low, 2s to high, and advance mid."
        }
    ],

    "bfs": [
        {
            "id": 127,
            "title": "Word Ladder",
            "slug": "word-ladder",
            "url": "https://leetcode.com/problems/word-ladder/",
            "difficulty": "Hard",
            "acceptance_rate": "39.5%",
            "topic_tags": ["Hash Table", "String", "Breadth-First Search"],
            "description": "Given beginWord, endWord, and wordList, return the length of the shortest transformation sequence from beginWord to endWord.",
            "relevance": "Classic unweighted shortest path graph traversal solved with Breadth-First Search (or bidirectional BFS).",
            "sample_io": "Input: beginWord = 'hit', endWord = 'cog', wordList = ['hot','dot','dog','lot','log','cog'] | Output: 5",
            "approach_tip": "Queue stores (word, level). For each word, mutate each character 'a'..'z' and check membership in word set."
        },
        {
            "id": 994,
            "title": "Rotting Oranges",
            "slug": "rotting-oranges",
            "url": "https://leetcode.com/problems/rotting-oranges/",
            "difficulty": "Medium",
            "acceptance_rate": "54.8%",
            "topic_tags": ["Array", "Breadth-First Search", "Matrix"],
            "description": "Return the minimum number of minutes that must elapse until no cell has a fresh orange. If impossible, return -1.",
            "relevance": "Multi-source Breadth-First Search propagating level-by-level simultaneously across a grid.",
            "sample_io": "Input: grid = [[2,1,1],[1,1,0],[0,1,1]] | Output: 4",
            "approach_tip": "Push all initial rotten oranges (value 2) into the queue. Pop layer-by-layer, infecting adjacent fresh oranges."
        },
        {
            "id": 102,
            "title": "Binary Tree Level Order Traversal",
            "slug": "binary-tree-level-order-traversal",
            "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
            "difficulty": "Medium",
            "acceptance_rate": "67.4%",
            "topic_tags": ["Tree", "Breadth-First Search", "Binary Tree"],
            "description": "Given the root of a binary tree, return the level order traversal of its nodes' values (from left to right, level by level).",
            "relevance": "Canonical FIFO queue-driven BFS traversing hierarchy level by level.",
            "sample_io": "Input: root = [3,9,20,null,null,15,7] | Output: [[3],[9,20],[15,7]]",
            "approach_tip": "Loop while queue not empty: snapshot queue length for current level, pop each node, append child nodes."
        }
    ],

    "dfs": [
        {
            "id": 200,
            "title": "Number of Islands",
            "slug": "number-of-islands",
            "url": "https://leetcode.com/problems/number-of-islands/",
            "difficulty": "Medium",
            "acceptance_rate": "59.2%",
            "topic_tags": ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"],
            "description": "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.",
            "relevance": "Foundational connected components discovery using recursive Depth-First Search flood-fill.",
            "sample_io": "Input: grid = [['1','1','0'],['1','1','0'],['0','0','1']] | Output: 2",
            "approach_tip": "Iterate grid cells. When '1' found, increment count and trigger DFS to sink all connected '1's into '0's."
        },
        {
            "id": 133,
            "title": "Clone Graph",
            "slug": "clone-graph",
            "url": "https://leetcode.com/problems/clone-graph/",
            "difficulty": "Medium",
            "acceptance_rate": "57.8%",
            "topic_tags": ["Hash Table", "Depth-First Search", "Breadth-First Search", "Graph"],
            "description": "Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.",
            "relevance": "DFS traversal keeping a visited hash map to map original nodes to their cloned counterparts and avoid cycles.",
            "sample_io": "Input: adjList = [[2,4],[1,3],[2,4],[1,3]] | Output: [[2,4],[1,3],[2,4],[1,3]]",
            "approach_tip": "Use a dictionary {original_node: cloned_node}. If node already in visited map, return copy; else recurse on neighbors."
        }
    ],

    "topological_sort": [
        {
            "id": 207,
            "title": "Course Schedule",
            "slug": "course-schedule",
            "url": "https://leetcode.com/problems/course-schedule/",
            "difficulty": "Medium",
            "acceptance_rate": "47.3%",
            "topic_tags": ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"],
            "description": "There are numCourses courses labeled 0 to numCourses - 1. Given prerequisites array, determine if it is possible to finish all courses.",
            "relevance": "Classic cycle detection in a directed graph using Kahn's algorithm (indegree BFS) or 3-color DFS.",
            "sample_io": "Input: numCourses = 2, prerequisites = [[1,0]] | Output: true",
            "approach_tip": "Compute in-degree for all vertices. Push in-degree 0 vertices to queue. Process queue, decrementing neighbor in-degrees."
        },
        {
            "id": 210,
            "title": "Course Schedule II",
            "slug": "course-schedule-ii",
            "url": "https://leetcode.com/problems/course-schedule-ii/",
            "difficulty": "Medium",
            "acceptance_rate": "50.5%",
            "topic_tags": ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"],
            "description": "Return the ordering of courses you should take to finish all courses. If impossible, return an empty array.",
            "relevance": "Direct generation of a valid linear topological ordering from a Directed Acyclic Graph (DAG).",
            "sample_io": "Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]] | Output: [0,2,1,3]",
            "approach_tip": "Append vertices to output array as they are popped from the zero in-degree queue. Return array if count == numCourses."
        },
        {
            "id": 269,
            "title": "Alien Dictionary",
            "slug": "alien-dictionary",
            "url": "https://leetcode.com/problems/alien-dictionary/",
            "difficulty": "Hard",
            "acceptance_rate": "35.8%",
            "topic_tags": ["Array", "String", "Graph", "Topological Sort"],
            "description": "Given a list of words from an alien language's dictionary sorted lexicographically, derive the order of letters in this language.",
            "relevance": "Construct a character DAG from adjacent word character mismatches, then extract topological ordering.",
            "sample_io": "Input: words = ['wrt','wrf','er','ett','rftt'] | Output: 'wertf'",
            "approach_tip": "Compare adjacent words to find first differing characters, adding directed edges u -> v. Run topological sort."
        }
    ],

    "minimum_spanning_tree": [
        {
            "id": 1584,
            "title": "Min Cost to Connect All Points",
            "slug": "min-cost-to-connect-all-points",
            "url": "https://leetcode.com/problems/min-cost-to-connect-all-points/",
            "difficulty": "Medium",
            "acceptance_rate": "67.2%",
            "topic_tags": ["Array", "Union Find", "Graph", "Minimum Spanning Tree"],
            "description": "Given 2D points representing coordinates on a map, return the minimum cost to make all points connected with Manhattan distance costs.",
            "relevance": "Standard Minimum Spanning Tree problem solvable via Prim's Algorithm (with min-heap) or Kruskal's Algorithm (with Disjoint Set Union).",
            "sample_io": "Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]] | Output: 20",
            "approach_tip": "Prim's: Start from node 0, maintain min-heap of (distance, next_node), greedily add nearest unvisited point until all N connected."
        },
        {
            "id": 1135,
            "title": "Connecting Cities With Minimum Cost",
            "slug": "connecting-cities-with-minimum-cost",
            "url": "https://leetcode.com/problems/connecting-cities-with-minimum-cost/",
            "difficulty": "Medium",
            "acceptance_rate": "62.4%",
            "topic_tags": ["Union Find", "Graph", "Minimum Spanning Tree"],
            "description": "Given n cities and bidirectional connections with costs, return the minimum cost to connect all cities, or -1 if impossible.",
            "relevance": "Pure Kruskal's algorithm: sort edges by weight, iterate edges, and unify disjoint sets if no cycle is formed.",
            "sample_io": "Input: n = 3, connections = [[1,2,5],[1,3,6],[2,3,1]] | Output: 6",
            "approach_tip": "Sort connections by weight. Iterate: if find(u) != find(v), union(u,v) and accumulate cost. Stop when edges == n-1."
        }
    ],

    "disjoint_set_union": [
        {
            "id": 684,
            "title": "Redundant Connection",
            "slug": "redundant-connection",
            "url": "https://leetcode.com/problems/redundant-connection/",
            "difficulty": "Medium",
            "acceptance_rate": "63.8%",
            "topic_tags": ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"],
            "description": "Return an edge that can be removed so that the resulting graph is a tree of n nodes.",
            "relevance": "Find the edge that connects two nodes already belonging to the same connected component in Union-Find.",
            "sample_io": "Input: edges = [[1,2],[1,3],[2,3]] | Output: [2,3]",
            "approach_tip": "Initialize DSU. For each edge (u, v), if find(u) == find(v), that edge creates a cycle and is redundant."
        },
        {
            "id": 128,
            "title": "Longest Consecutive Sequence",
            "slug": "longest-consecutive-sequence",
            "url": "https://leetcode.com/problems/longest-consecutive-sequence/",
            "difficulty": "Medium",
            "acceptance_rate": "47.6%",
            "topic_tags": ["Array", "Hash Table", "Union Find"],
            "description": "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence in O(n) time.",
            "relevance": "Can be solved using Union-Find uniting x with x+1, or hash set checking sequence starts.",
            "sample_io": "Input: nums = [100,4,200,1,3,2] | Output: 4",
            "approach_tip": "Put numbers in set. Only start counting sequence from num if (num - 1) is not in set to ensure O(N) linear time."
        }
    ],

    "knapsack_dp": [
        {
            "id": 416,
            "title": "Partition Equal Subset Sum",
            "slug": "partition-equal-subset-sum",
            "url": "https://leetcode.com/problems/partition-equal-subset-sum/",
            "difficulty": "Medium",
            "acceptance_rate": "46.8%",
            "topic_tags": ["Array", "Dynamic Programming"],
            "description": "Given an integer array nums, return true if you can partition the array into two subsets with equal sum.",
            "relevance": "Reducible directly to 0/1 Knapsack where target weight is sum(nums) // 2.",
            "sample_io": "Input: nums = [1,5,11,5] | Output: true",
            "approach_tip": "If sum is odd, return False. Maintain boolean DP array dp[j] indicating if subset sum j is achievable."
        },
        {
            "id": 322,
            "title": "Coin Change",
            "slug": "coin-change",
            "url": "https://leetcode.com/problems/coin-change/",
            "difficulty": "Medium",
            "acceptance_rate": "44.6%",
            "topic_tags": ["Array", "Dynamic Programming", "Breadth-First Search"],
            "description": "Given integer array coins and target amount, return the fewest number of coins that you need to make up that amount.",
            "relevance": "Classic Unbounded Knapsack problem with infinite item reuse.",
            "sample_io": "Input: coins = [1,2,5], amount = 11 | Output: 3",
            "approach_tip": "dp[i] = min(dp[i], dp[i - coin] + 1) for coin in coins, initialized to infinity."
        },
        {
            "id": 494,
            "title": "Target Sum",
            "slug": "target-sum",
            "url": "https://leetcode.com/problems/target-sum/",
            "difficulty": "Medium",
            "acceptance_rate": "46.9%",
            "topic_tags": ["Array", "Dynamic Programming", "Backtracking"],
            "description": "Assign '+' or '-' to each number in nums to evaluate to target. Return the number of different expressions.",
            "relevance": "Mathematical transformation into 0/1 Knapsack counting subset sums equaling (sum + target) // 2.",
            "sample_io": "Input: nums = [1,1,1,1,1], target = 3 | Output: 5",
            "approach_tip": "Let P be positive subset, N be negative. P - N = target => 2P = target + sum(nums). Solve subset sum."
        }
    ],

    "dynamic_programming": [
        {
            "id": 1143,
            "title": "Longest Common Subsequence",
            "slug": "longest-common-subsequence",
            "url": "https://leetcode.com/problems/longest-common-subsequence/",
            "difficulty": "Medium",
            "acceptance_rate": "58.2%",
            "topic_tags": ["String", "Dynamic Programming"],
            "description": "Given two strings text1 and text2, return the length of their longest common subsequence.",
            "relevance": "Standard 2D dynamic programming grid evaluating matching characters versus optimal sub-problems.",
            "sample_io": "Input: text1 = 'abcde', text2 = 'ace' | Output: 3",
            "approach_tip": "If text1[i] == text2[j], dp[i][j] = 1 + dp[i-1][j-1]; else dp[i][j] = max(dp[i-1][j], dp[i][j-1])."
        },
        {
            "id": 300,
            "title": "Longest Increasing Subsequence",
            "slug": "longest-increasing-subsequence",
            "url": "https://leetcode.com/problems/longest-increasing-subsequence/",
            "difficulty": "Medium",
            "acceptance_rate": "55.8%",
            "topic_tags": ["Array", "Binary Search", "Dynamic Programming"],
            "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence in O(n log n).",
            "relevance": "Patience sorting / DP with binary search replacement (bisect_left).",
            "sample_io": "Input: nums = [10,9,2,5,3,7,101,18] | Output: 4",
            "approach_tip": "Maintain tails array of smallest tail of all increasing subsequences of length i. Use binary search to update tails."
        },
        {
            "id": 72,
            "title": "Edit Distance",
            "slug": "edit-distance",
            "url": "https://leetcode.com/problems/edit-distance/",
            "difficulty": "Medium",
            "acceptance_rate": "56.7%",
            "topic_tags": ["String", "Dynamic Programming"],
            "description": "Given word1 and word2, return the minimum operations (insert, delete, replace) required to convert word1 to word2.",
            "relevance": "Levenshtein distance algorithm utilizing 2D dynamic programming grid.",
            "sample_io": "Input: word1 = 'horse', word2 = 'ros' | Output: 3",
            "approach_tip": "dp[i][j] = 1 + min(insert dp[i][j-1], delete dp[i-1][j], replace dp[i-1][j-1]) when characters differ."
        }
    ],

    "kadane": [
        {
            "id": 53,
            "title": "Maximum Subarray",
            "slug": "maximum-subarray",
            "url": "https://leetcode.com/problems/maximum-subarray/",
            "difficulty": "Medium",
            "acceptance_rate": "51.1%",
            "topic_tags": ["Array", "Divide and Conquer", "Dynamic Programming"],
            "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
            "relevance": "The exact textbook problem formulated and solved by Kadane's Algorithm in linear O(N) time.",
            "sample_io": "Input: nums = [-2,1,-3,4,-1,2,1,-5,4] | Output: 6",
            "approach_tip": "Track current_sum = max(num, current_sum + num) and global_max = max(global_max, current_sum)."
        },
        {
            "id": 918,
            "title": "Maximum Sum Circular Subarray",
            "slug": "maximum-sum-circular-subarray",
            "url": "https://leetcode.com/problems/maximum-sum-circular-subarray/",
            "difficulty": "Medium",
            "acceptance_rate": "45.2%",
            "topic_tags": ["Array", "Divide and Conquer", "Dynamic Programming", "Queue", "Monotonic Queue"],
            "description": "Given a circular integer array nums, return the maximum possible sum of a non-empty subarray of nums.",
            "relevance": "Kadane's algorithm run twice: once for max subarray, once for min subarray to compute total_sum - min_subarray.",
            "sample_io": "Input: nums = [1,-2,3,-2] | Output: 3",
            "approach_tip": "Max circular subarray is either max_kadane or (total_sum - min_kadane) if total_sum != min_kadane."
        }
    ],

    "greedy": [
        {
            "id": 435,
            "title": "Non-overlapping Intervals",
            "slug": "non-overlapping-intervals",
            "url": "https://leetcode.com/problems/non-overlapping-intervals/",
            "difficulty": "Medium",
            "acceptance_rate": "53.8%",
            "topic_tags": ["Array", "Dynamic Programming", "Greedy", "Sorting"],
            "description": "Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest non-overlapping.",
            "relevance": "Classic interval scheduling / activity selection algorithm greedily choosing intervals by earliest end time.",
            "sample_io": "Input: intervals = [[1,2],[2,3],[3,4],[1,3]] | Output: 1",
            "approach_tip": "Sort intervals by end time. Keep track of last valid interval's end; skip any interval whose start < last_end."
        },
        {
            "id": 55,
            "title": "Jump Game",
            "slug": "jump-game",
            "url": "https://leetcode.com/problems/jump-game/",
            "difficulty": "Medium",
            "acceptance_rate": "38.9%",
            "topic_tags": ["Array", "Dynamic Programming", "Greedy"],
            "description": "You are given an integer array nums where nums[i] is your max jump length. Return true if you can reach the last index.",
            "relevance": "Greedy frontier tracking maintaining the maximum reachable index at every step.",
            "sample_io": "Input: nums = [2,3,1,1,4] | Output: true",
            "approach_tip": "Iterate i: if i > max_reach, return False; update max_reach = max(max_reach, i + nums[i])."
        }
    ],

    "backtracking": [
        {
            "id": 51,
            "title": "N-Queens",
            "slug": "n-queens",
            "url": "https://leetcode.com/problems/n-queens/",
            "difficulty": "Hard",
            "acceptance_rate": "68.9%",
            "topic_tags": ["Array", "Backtracking"],
            "description": "Place n queens on an n x n chessboard such that no two queens attack each other. Return all distinct solutions.",
            "relevance": "The archetypal recursive backtracking algorithm with pruning across columns and diagonals.",
            "sample_io": "Input: n = 4 | Output: [['.Q..','...Q','Q...','..Q.'],['..Q.','Q...','...Q','.Q..']]",
            "approach_tip": "Place row by row. Track occupied columns, positive diagonals (row + col), and negative diagonals (row - col) in sets."
        },
        {
            "id": 46,
            "title": "Permutations",
            "slug": "permutations",
            "url": "https://leetcode.com/problems/permutations/",
            "difficulty": "Medium",
            "acceptance_rate": "78.4%",
            "topic_tags": ["Array", "Backtracking"],
            "description": "Given an array nums of distinct integers, return all the possible permutations in any order.",
            "relevance": "Canonical backtracking state space tree traversal exploring all N! permutations.",
            "sample_io": "Input: nums = [1,2,3] | Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]",
            "approach_tip": "Swap elements in-place or maintain a visited boolean array, recursing and then undoing choices."
        },
        {
            "id": 78,
            "title": "Subsets",
            "slug": "subsets",
            "url": "https://leetcode.com/problems/subsets/",
            "difficulty": "Medium",
            "acceptance_rate": "77.9%",
            "topic_tags": ["Array", "Backtracking", "Bit Manipulation"],
            "description": "Given an integer array nums of unique elements, return all possible subsets (the power set).",
            "relevance": "Binary decision tree backtracking generating 2^N elements.",
            "sample_io": "Input: nums = [1,2,3] | Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]",
            "approach_tip": "Recurse with start index: at each step add current path to results, iterate remaining elements, recurse, pop."
        }
    ],

    "two_pointers": [
        {
            "id": 15,
            "title": "3Sum",
            "slug": "3sum",
            "url": "https://leetcode.com/problems/3sum/",
            "difficulty": "Medium",
            "acceptance_rate": "35.1%",
            "topic_tags": ["Array", "Two Pointers", "Sorting"],
            "description": "Given an integer array nums, return all unique triplets [nums[i], nums[j], nums[k]] such that they sum to 0.",
            "relevance": "Sort + fixed outer loop with converging two pointers running in O(N^2) time.",
            "sample_io": "Input: nums = [-1,0,1,2,-1,-4] | Output: [[-1,-1,2],[-1,0,1]]",
            "approach_tip": "Sort array. For each i, use left = i+1 and right = n-1 pointers. Skip duplicates for all three pointers."
        },
        {
            "id": 11,
            "title": "Container With Most Water",
            "slug": "container-with-most-water",
            "url": "https://leetcode.com/problems/container-with-most-water/",
            "difficulty": "Medium",
            "acceptance_rate": "55.6%",
            "topic_tags": ["Array", "Two Pointers", "Greedy"],
            "description": "Find two lines that together with the x-axis form a container, such that the container contains the most water.",
            "relevance": "Greedy two-pointer contraction starting at boundaries and inward-advancing the shorter pillar.",
            "sample_io": "Input: height = [1,8,6,2,5,4,8,3,7] | Output: 49",
            "approach_tip": "Calculate area = (right - left) * min(h[left], h[right]). Always advance the pointer pointing to the smaller height."
        }
    ],

    "sliding_window": [
        {
            "id": 3,
            "title": "Longest Substring Without Repeating Characters",
            "slug": "longest-substring-without-repeating-characters",
            "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            "difficulty": "Medium",
            "acceptance_rate": "35.2%",
            "topic_tags": ["Hash Table", "String", "Sliding Window"],
            "description": "Given a string s, find the length of the longest substring without duplicate characters.",
            "relevance": "Archetypal variable-length sliding window dynamically adjusting the left boundary based on character occurrences.",
            "sample_io": "Input: s = 'abcabcbb' | Output: 3",
            "approach_tip": "Store {char: last_seen_index}. If char seen in current window, jump left = char_map[char] + 1."
        },
        {
            "id": 76,
            "title": "Minimum Window Substring",
            "slug": "minimum-window-substring",
            "url": "https://leetcode.com/problems/minimum-window-substring/",
            "difficulty": "Hard",
            "acceptance_rate": "42.8%",
            "topic_tags": ["Hash Table", "String", "Sliding Window"],
            "description": "Given two strings s and t, return the minimum window substring of s such that every character in t is included.",
            "relevance": "Master sliding window with frequency matching map and condition satisfaction counting.",
            "sample_io": "Input: s = 'ADOBECODEBANC', t = 'ABC' | Output: 'BANC'",
            "approach_tip": "Expand right until window contains all required chars, then contract left to minimize window while maintaining criteria."
        }
    ],

    "metaheuristic_rl": [
        {
            "id": 847,
            "title": "Shortest Path Visiting All Nodes",
            "slug": "shortest-path-visiting-all-nodes",
            "url": "https://leetcode.com/problems/shortest-path-visiting-all-nodes/",
            "difficulty": "Hard",
            "acceptance_rate": "62.4%",
            "topic_tags": ["Dynamic Programming", "Bit Manipulation", "Breadth-First Search", "Graph", "Bitmask"],
            "description": "Given an undirected graph, return the length of the shortest path that visits every node at least once.",
            "relevance": "NP-hard Traveling Salesperson Problem (TSP) formulation directly matching combinatorial optimization tackled by GA-RL and simulated annealing.",
            "sample_io": "Input: graph = [[1,2,3],[0],[0],[0]] | Output: 4",
            "approach_tip": "Use BFS with state (current_node, visited_bitmask) initialized with all nodes at bitmask (1 << node)."
        },
        {
            "id": 174,
            "title": "Dungeon Game",
            "slug": "dungeon-game",
            "url": "https://leetcode.com/problems/dungeon-game/",
            "difficulty": "Hard",
            "acceptance_rate": "38.7%",
            "topic_tags": ["Array", "Dynamic Programming", "Matrix"],
            "description": "Determine the knight's minimum initial health so that he can rescue the princess located at bottom-right cell.",
            "relevance": "Markov Decision Process / Bellman backward induction value iteration on a 2D state space.",
            "sample_io": "Input: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]] | Output: 7",
            "approach_tip": "Compute backward from bottom-right target: health needed entering cell is max(1, min_next_health - cell_value)."
        },
        {
            "id": 698,
            "title": "Partition to K Equal Sum Subsets",
            "slug": "partition-to-k-equal-sum-subsets",
            "url": "https://leetcode.com/problems/partition-to-k-equal-sum-subsets/",
            "difficulty": "Medium",
            "acceptance_rate": "38.5%",
            "topic_tags": ["Array", "Dynamic Programming", "Backtracking", "Bitmask"],
            "description": "Given an integer array nums and integer k, return true if possible to divide nums into k non-empty subsets whose sums are all equal.",
            "relevance": "Combinatorial bin-packing optimization problem matching Genetic Algorithm chromosome allocation.",
            "sample_io": "Input: nums = [4,3,2,3,5,2,1], k = 4 | Output: true",
            "approach_tip": "Sort nums descending. Prune whenever current bin + nums[i] exceeds target sum."
        }
    ],

    "string_matching": [
        {
            "id": 28,
            "title": "Find the Index of the First Occurrence in a String",
            "slug": "find-the-index-of-the-first-occurrence-in-a-string",
            "url": "https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/",
            "difficulty": "Easy",
            "acceptance_rate": "43.1%",
            "topic_tags": ["Two Pointers", "String", "String Matching"],
            "description": "Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1.",
            "relevance": "Classic string search solvable via KMP (Knuth-Morris-Pratt) LPS array in linear O(N + M) time.",
            "sample_io": "Input: haystack = 'sadbutsad', needle = 'sad' | Output: 0",
            "approach_tip": "Precompute longest prefix suffix (LPS) table of needle to skip redundant character comparisons."
        },
        {
            "id": 214,
            "title": "Shortest Palindrome",
            "slug": "shortest-palindrome",
            "url": "https://leetcode.com/problems/shortest-palindrome/",
            "difficulty": "Hard",
            "acceptance_rate": "34.5%",
            "topic_tags": ["String", "Rolling Hash", "String Matching", "Hash Function"],
            "description": "Find the shortest palindrome you can build by adding characters in front of string s.",
            "relevance": "Advanced KMP application: build string s + '#' + rev(s) and compute the LPS array to find longest prefix palindrome.",
            "sample_io": "Input: s = 'aacecaaa' | Output: 'aaacecaaa'",
            "approach_tip": "Run KMP prefix function on s + '#' + s[::-1]. The last LPS value gives the length of palindrome prefix."
        }
    ],

    "tree_bst": [
        {
            "id": 98,
            "title": "Validate Binary Search Tree",
            "slug": "validate-binary-search-tree",
            "url": "https://leetcode.com/problems/validate-binary-search-tree/",
            "difficulty": "Medium",
            "acceptance_rate": "33.1%",
            "topic_tags": ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"],
            "description": "Given the root of a binary tree, determine if it is a valid binary search tree (BST).",
            "relevance": "In-order traversal yielding strictly monotonic ascending sequence or recursive lower/upper bound validation.",
            "sample_io": "Input: root = [2,1,3] | Output: true",
            "approach_tip": "Pass (node, min_val, max_val) bounds down the recursion: check min_val < node.val < max_val."
        },
        {
            "id": 236,
            "title": "Lowest Common Ancestor of a Binary Tree",
            "slug": "lowest-common-ancestor-of-a-binary-tree",
            "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
            "difficulty": "Medium",
            "acceptance_rate": "62.3%",
            "topic_tags": ["Tree", "Depth-First Search", "Binary Tree"],
            "description": "Given a binary tree and two nodes p and q, find the lowest common ancestor (LCA) node.",
            "relevance": "Post-order tree traversal aggregating subtree findings.",
            "sample_io": "Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1 | Output: 3",
            "approach_tip": "If root is None, p, or q, return root. Recurse left and right. If both return non-null, root is the LCA."
        }
    ]
}


def get_leetcode_problems_for_algorithm(
    algorithm_name: str,
    category: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    description: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Intelligently select matching LeetCode problems for any CS algorithm query.
    Performs normalized keyword matching, category matching, and intelligent fallback.
    """
    raw_name = (algorithm_name or "").lower().strip()
    # Normalize hyphens, underscores, and punctuation to spaces
    name_clean = re.sub(r"[^a-z0-9]+", " ", raw_name).strip()
    cat_clean = re.sub(r"[^a-z0-9]+", " ", (category or "").lower()).strip()
    kw_clean = " ".join([re.sub(r"[^a-z0-9]+", " ", str(k).lower()) for k in (keywords or [])])
    desc_clean = re.sub(r"[^a-z0-9]+", " ", (description or "").lower()).strip()
    full_text = f"{name_clean} {cat_clean} {kw_clean} {desc_clean}"

    # 1. Direct algorithm key pattern matching
    if any(k in name_clean for k in ["manacher", "palindrom", "longest palindromic"]):
        return LEETCODE_DATABASE["palindrome"]

    if any(k in name_clean for k in ["skip list", "skiplist"]):
        return LEETCODE_DATABASE["skiplist"]

    if any(k in name_clean for k in ["tarjan", "bridge", "biconnected", "articulation"]):
        return LEETCODE_DATABASE["graph_bridges"]

    if any(k in name_clean for k in ["hopcroft", "hungarian", "bipartite", "assignment", "kuhn"]):
        return LEETCODE_DATABASE["bipartite_matching"]

    if any(k in name_clean for k in ["fft", "fourier", "cooley", "tukey", "karatsuba", "strassen"]):
        return LEETCODE_DATABASE["fast_fourier_transform"]

    if any(k in name_clean for k in ["simplex", "linear programming", "operations research"]):
        return LEETCODE_DATABASE["metaheuristic_rl"]
    if any(k in name_clean for k in ["dijkstra", "shortest path", "routing optimizer", "traffic", "network delay"]):
        return LEETCODE_DATABASE["dijkstra"]

    if any(k in name_clean for k in ["bellman", "ford", "negative cycle"]):
        return LEETCODE_DATABASE["bellman_ford"]

    if any(k in name_clean for k in ["floyd", "warshall", "all pairs shortest", "transitive closure"]):
        return LEETCODE_DATABASE["floyd_warshall"]

    if any(k in name_clean for k in ["binary search", "bsearch", "rotated sorted", "median"]):
        return LEETCODE_DATABASE["binary_search"]

    if any(k in name_clean for k in ["merge sort", "mergesort", "sort list"]):
        return LEETCODE_DATABASE["merge_sort"]

    if any(k in name_clean for k in ["quick sort", "quicksort", "quickselect", "kth largest", "sort colors"]):
        return LEETCODE_DATABASE["quick_sort"]

    if any(k in name_clean for k in ["kruskal", "prim", "minimum spanning tree", "mst", "connect all points"]):
        return LEETCODE_DATABASE["minimum_spanning_tree"]

    if any(k in name_clean for k in ["union find", "disjoint set", "dsu", "connected components", "redundant connection"]):
        return LEETCODE_DATABASE["disjoint_set_union"]

    if any(k in name_clean for k in ["knapsack", "subset sum", "coin change", "partition equal"]):
        return LEETCODE_DATABASE["knapsack_dp"]

    if any(k in name_clean for k in ["kadane", "max subarray", "maximum subarray"]):
        return LEETCODE_DATABASE["kadane"]

    if any(k in name_clean for k in ["topological", "kahn", "course schedule", "dependency"]):
        return LEETCODE_DATABASE["topological_sort"]

    if any(k in name_clean for k in ["bfs", "breadth first", "level order", "word ladder", "rotting orange"]):
        return LEETCODE_DATABASE["bfs"]

    if any(k in name_clean for k in ["dfs", "depth first", "flood fill", "number of islands", "clone graph"]):
        return LEETCODE_DATABASE["dfs"]

    if any(k in name_clean for k in ["n queen", "n queens", "backtrack", "permutation", "subset", "combination sum"]):
        return LEETCODE_DATABASE["backtracking"]

    if any(k in name_clean for k in ["two pointer", "3sum", "three sum", "container with most water", "rain water"]):
        return LEETCODE_DATABASE["two_pointers"]

    if any(k in name_clean for k in ["sliding window", "longest substring", "minimum window"]):
        return LEETCODE_DATABASE["sliding_window"]

    if any(k in name_clean for k in ["genetic", "reinforcement learning", "ga rl", "garl", "metaheuristic", "annealing", "particle swarm", "pso", "tsp", "traveling salesman", "vrp", "vehicle routing", "optimization", "foraging", "firefly", "harmony", "colony", "bee", "cuckoo", "evolutionary"]):
        return LEETCODE_DATABASE["metaheuristic_rl"]

    if any(k in name_clean for k in ["kmp", "knuth", "morris", "pratt", "string matching", "rabin karp", "palindrome"]):
        return LEETCODE_DATABASE["string_matching"]

    if any(k in name_clean for k in ["bst", "binary search tree", "tree", "lowest common ancestor", "lca"]):
        return LEETCODE_DATABASE["tree_bst"]

    if any(k in name_clean for k in ["greedy", "interval", "activity selection", "jump game"]):
        return LEETCODE_DATABASE["greedy"]

    if any(k in name_clean for k in ["longest common subsequence", "lcs", "longest increasing subsequence", "lis", "edit distance", "dynamic programming", "dp"]):
        return LEETCODE_DATABASE["dynamic_programming"]

    # 2. Broader category & keyword inference
    if "graph" in cat_clean or "graph" in kw_clean or "graph" in desc_clean:
        return LEETCODE_DATABASE["dijkstra"]

    if "sort" in cat_clean or "sort" in kw_clean or "sort" in desc_clean:
        return LEETCODE_DATABASE["merge_sort"]

    if "search" in cat_clean or "search" in kw_clean or "search" in desc_clean:
        return LEETCODE_DATABASE["binary_search"]

    if "dp" in cat_clean or "dynamic" in cat_clean or "optimization" in cat_clean or "optimization" in desc_clean:
        return LEETCODE_DATABASE["knapsack_dp"]

    if "tree" in cat_clean or "tree" in kw_clean:
        return LEETCODE_DATABASE["tree_bst"]

    if "string" in cat_clean or "string" in kw_clean:
        return LEETCODE_DATABASE["string_matching"]

    # 3. Dynamic algorithm synthesizer for custom queries
    return [
        {
            "id": 847,
            "title": "Shortest Path Visiting All Nodes",
            "slug": "shortest-path-visiting-all-nodes",
            "url": "https://leetcode.com/problems/shortest-path-visiting-all-nodes/",
            "difficulty": "Hard",
            "acceptance_rate": "62.4%",
            "topic_tags": ["Graph", "Dynamic Programming", "Bitmask", "Breadth-First Search"],
            "description": f"Find the shortest path visiting all vertices for optimization algorithms like {algorithm_name}.",
            "relevance": f"Primary algorithmic benchmark for advanced optimization strategies and {algorithm_name}.",
            "sample_io": "Input: graph = [[1,2,3],[0],[0],[0]] | Output: 4",
            "approach_tip": "Model the state using bitmasks to track visited nodes while minimizing total traversal path length."
        },
        {
            "id": 743,
            "title": "Network Delay Time",
            "slug": "network-delay-time",
            "url": "https://leetcode.com/problems/network-delay-time/",
            "difficulty": "Medium",
            "acceptance_rate": "54.2%",
            "topic_tags": ["Graph", "Shortest Path", "Heap (Priority Queue)"],
            "description": f"Calculate minimum latency across nodes using optimal shortest path heuristics.",
            "relevance": f"Essential network routing benchmark closely aligned with {algorithm_name}.",
            "sample_io": "Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 | Output: 2",
            "approach_tip": "Use a priority queue to greedily visit minimal cost branches."
        }
    ]
