def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Basic functionality
    expected_answer = "Hello World"
    test_case_input = ["Hello", "World"]
    if solution(test_case_input) == expected_answer:
        passed.append("Solution has passed test case with input ['Hello', 'World'] and expected result 'Hello World'")
    else:
        not_passed.append("Solution has not passed test case with input ['Hello', 'World'] result 'Hello World'")

    # Test case 2: Single word
    expected_answer = "Hello"
    test_case_input = ["Hello"]
    if solution(test_case_input) == expected_answer:
        passed.append("Solution has passed test case with input ['Hello'] and expected result 'Hello'")
    else:
        not_passed.append("Solution has not passed test case with input ['Hello'] result 'Hello'")

    # Test case 3: Empty list
    expected_answer = ""
    test_case_input = []
    if solution(test_case_input) == expected_answer:
        passed.append("Solution has passed test case with input [] and expected result ''")
    else:
        not_passed.append("Solution has not passed test case with input [] result ''")

    # Test case 4: Multiple words
    expected_answer = "Hello World from Python"
    test_case_input = ["Hello", "World", "from", "Python"]
    if solution(test_case_input) == expected_answer:
        passed.append("Solution has passed test case with input ['Hello', 'World', 'from', 'Python'] and expected result 'Hello World from Python'")
    else:
        not_passed.append("Solution has not passed test case with input ['Hello', 'World', 'from', 'Python'] result 'Hello World from Python'")

    return passed, not_passed