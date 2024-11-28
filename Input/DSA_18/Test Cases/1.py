def test_solution(solution):
    class Graph:
        def __init__(self):
            self.graph = {}

        def add_edge(self, u, v):
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append(v)
            self.graph[v].append(u)  # For undirected graph

        def get_edges(self):
            return self.graph

    # Test Case 1: Simple graph
    g1 = Graph()
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 2)
    g1.add_edge(1, 3)
    g1.add_edge(2, 4)
    expected_output1 = [0, 1, 2, 3, 4]  # BFS starting from node 0
    if solution(g1.get_edges(), 0) == expected_output1:
        print("Test Case 1 Passed")
    else:
        print("Test Case 1 Failed")

    # Test Case 2: Graph with disconnected components
    g2 = Graph()
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(3, 4)
    expected_output2 = [3, 4]  # BFS starting from node 3
    if solution(g2.get_edges(), 3) == expected_output2:
        print("Test Case 2 Passed")
    else:
        print("Test Case 2 Failed")

    # Test Case 3: Graph with a single node
    g3 = Graph()
    expected_output3 = [0]  # BFS starting from node 0
    if solution({0: []}, 0) == expected_output3:
        print("Test Case 3 Passed")
    else:
        print("Test Case 3 Failed")

    # Test Case 4: Empty graph
    g4 = Graph()
    expected_output4 = []  # BFS starting from any node in an empty graph
    if solution(g4.get_edges(), 0) == expected_output4:
        print("Test Case 4 Passed")
    else:
        print("Test Case 4 Failed")

    # Test Case 5: Graph with cycles
    g5 = Graph()
    g5.add_edge(0, 1)
    g5.add_edge(1, 2)
    g5.add_edge(2, 0)  # Cycle here
    g5.add_edge(1, 3)
    expected_output5 = [0, 1, 2, 3]  # BFS starting from node 0
    if solution(g5.get_edges(), 0) == expected_output5:
        print("Test Case 5 Passed")
    else:
        print("Test Case 5 Failed")