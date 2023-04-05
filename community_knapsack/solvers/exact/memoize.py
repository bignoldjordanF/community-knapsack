from typing import List, Tuple, Dict


def memoization(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    also known as top-down dynamic programming.

    The algorithm explores all possible allocations through branches in a recursion tree, i.e., we create two
    branches: one that includes the current item and one that does not. We store the results of branches that have
    already been explored thus avoiding re-computation and upper bounding the time complexity of the algorithm to
    be pseudo-polynomial in the number of items and capacity, i.e., O(nC).

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of item indexes and its overall value.
    """
    num_items: int = len(values)

    # Store the maximum value achievable for any sub-problem:
    matrix: List[List[int]] = [
        [-1 for _ in range(capacity + 1)]
        for _ in range(num_items + 1)
    ]

    def explore(i: int, j: int) -> int:
        # Avoid re-computation through
        # memoization:
        if matrix[i][j] != -1:
            return matrix[i][j]

        # (Base Case)
        # We have no more items or
        # capacity to consider:
        if i == 0 or j == 0:
            matrix[i][j] = 0
            return matrix[i][j]

        # (Recursive Case 1)
        # We cannot fit the current
        # item, so we must exclude:
        if weights[i - 1] > j:
            matrix[i][j] = explore(i - 1, j)
            return matrix[i][j]

        # (Recursive Case 2)
        # Include the current item if
        # and only if it leads to a
        # larger value than excluding:
        exclude: int = explore(i - 1, j)
        include: int = explore(i - 1, j - weights[i - 1]) + values[i - 1]

        if include > exclude:
            # We store the updated allocation and value:
            matrix[i][j] = include
            return matrix[i][j]

        matrix[i][j] = exclude
        return matrix[i][j]

    # We first consider one (the last) item
    # and have full capacity:
    best_value: int = explore(num_items, capacity)
    allocation: List[int] = []

    # Backtrack the matrix to find an allocation
    # with `best_value` overall value:
    i: int = num_items
    j: int = capacity
    while i > 0 and j > 0:
        if matrix[i][j] != matrix[i - 1][j]:
            allocation.append(i - 1)
            j -= weights[i - 1]
        i -= 1

    return allocation, best_value


def multi_memoization(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm that improves upon the brute force algorithm for a faster result. This is also known as a
    top-down dynamic programming approach.

    The algorithm explores all possible allocations through branches in a recursion tree, i.e., we create two
    branches: one that includes the current item and one that does not. We store the results of branches that have
    already been explored thus avoiding re-computation. In the worst case, we explore every possible item and every
    possible capacity, and thus the time complexity is O(n * max(capacities)^d), where d is the number of capacities,
    in the worst case.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_items: int = len(values)

    # Store the maximum value achievable for any sub-problem.
    # This approach uses a dictionary to avoid dealing with
    # a rigid d-dimensional matrix:
    memo: Dict[Tuple[int, Tuple[int]], Tuple[List[int], int]] = {}

    def explore(i: int, j: List[int]):
        # Avoid re-computation through memoization:
        sub_problem: Tuple[int, Tuple[int]] = (i, tuple(j))
        if sub_problem in memo:
            return memo[sub_problem]

        # (Base Case)
        # We have no more items or capacity to consider:
        if i == 0 or any(capacity == 0 for capacity in j):
            memo[sub_problem] = ([], 0)
            return memo[sub_problem]

        # (Recursive Case 1)
        # We cannot fit the current item, so we must exclude:
        if any(weights[cid][i - 1] > capacity for cid, capacity in enumerate(j)):
            memo[sub_problem] = explore(i - 1, j)
            return memo[sub_problem]

        # (Recursive Case 2)
        # Find the maximum values from including and excluding. We must update
        # the capacity list to reflect including the item:
        j_updated: List[int] = [capacity - weights[cid][i - 1] for cid, capacity in enumerate(j)]
        include: Tuple[List[int], int] = explore(i - 1, j_updated)
        exclude: Tuple[List[int], int] = explore(i - 1, j)

        # Accept the allocation that includes the current item if and only if
        # it has a higher overall value, otherwise accept the exclusion:
        if include[1] + values[i - 1] > exclude[1]:
            memo[sub_problem] = (include[0] + [i - 1], include[1] + values[i - 1])
            return memo[sub_problem]

        memo[sub_problem] = exclude
        return memo[sub_problem]

    # We first consider one (the last) item
    # and have full capacity:
    return explore(num_items, capacities)
