def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Simple graph
    graph1 = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    start1 = 'A'
    expected1 = ['A', 'B', 'C', 'D', 'E', 'F']
    if solution(graph1, start1) == expected1:
        passed.append("Solution has passed test case with parameters graph1, start1 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph1, start1 result " + str(expected1))

    # Test case 2: Disconnected graph
    graph2 = {
        'A': ['B'],
        'B': ['A'],
        'C': ['D'],
        'D': ['C']
    }
    start2 = 'A'
    expected2 = ['A', 'B']
    if solution(graph2, start2) == expected2:
        passed.append("Solution has passed test case with parameters graph2, start2 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph2, start2 result " + str(expected2))

    # Test case 3: Single node graph
    graph3 = {
        'A': []
    }
    start3 = 'A'
    expected3 = ['A']
    if solution(graph3, start3) == expected3:
        passed.append("Solution has passed test case with parameters graph3, start3 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph3, start3 result " + str(expected3))

    return passed, not_passed