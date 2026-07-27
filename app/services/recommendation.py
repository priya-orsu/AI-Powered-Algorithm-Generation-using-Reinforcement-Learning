def recommend(category):

    recommendations = {

        "Graph": [
            "Dijkstra",
            "Bellman Ford",
            "Prim",
            "Kruskal",
            "Floyd Warshall"
        ],

        "Sorting": [
            "Merge Sort",
            "Quick Sort",
            "Heap Sort",
            "Insertion Sort"
        ]
    }

    return recommendations.get(category, [])