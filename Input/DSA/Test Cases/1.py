def test_solution(solution):
    class ListNode:
        def __init__(self, value=0, next=None):
            self.value = value
            self.next = next

    def linked_list_to_list(head):
        result = []
        current = head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def list_to_linked_list(lst):
        if not lst:
            return None
        head = ListNode(lst[0])
        current = head
        for value in lst[1:]:
            current.next = ListNode(value)
            current = current.next
        return head

    # Test case 1: Normal case with multiple elements
    input_list = [1, 2, 3, 4, 5]
    expected_output = [5, 4, 3, 2, 1]
    head = list_to_linked_list(input_list)
    reversed_head = solution(head)
    assert linked_list_to_list(reversed_head) == expected_output, f"Failed on test case 1"

    # Test case 2: Single element
    input_list = [1]
    expected_output = [1]
    head = list_to_linked_list(input_list)
    reversed_head = solution(head)
    assert linked_list_to_list(reversed_head) == expected_output, f"Failed on test case 2"

    # Test case 3: Empty list
    input_list = []
    expected_output = []
    head = list_to_linked_list(input_list)
    reversed_head = solution(head)
    assert linked_list_to_list(reversed_head) == expected_output, f"Failed on test case 3"

    # Test case 4: Two elements
    input_list = [1, 2]
    expected_output = [2, 1]
    head = list_to_linked_list(input_list)
    reversed_head = solution(head)
    assert linked_list_to_list(reversed_head) == expected_output, f"Failed on test case 4"

    # Test case 5: List with duplicate elements
    input_list = [1, 2, 2, 3]
    expected_output = [3, 2, 2, 1]
    head = list_to_linked_list(input_list)
    reversed_head = solution(head)
    assert linked_list_to_list(reversed_head) == expected_output, f"Failed on test case 5"

    print("All test cases passed!")

# Call the test function with the solution function
# test_solution(solution)