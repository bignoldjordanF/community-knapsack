from typing import List, Tuple


def memoization(capacity, weights, values):
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
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """

    # Store the maximum value achievable for any sub-problem:
    matrix: List[List[Tuple[List[int], int]]] = [
        [([], -1) for _ in range(capacity + 1)]
        for _ in range(len(values) + 1)
    ]

    def explore(i, j):
        # Avoid re-computation through
        # memoization:
        if matrix[i][j][1] != -1:
            return matrix[i][j]

        # (Base Case)
        # We have no more items or
        # capacity to consider:
        if i == 0 or j == 0:
            matrix[i][j] = ([], 0)
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
        exclude: Tuple[List[int], int] = explore(i - 1, j)
        include: Tuple[List[int], int] = explore(i - 1, j - weights[i - 1])

        exclude_val: int = exclude[1]
        include_val: int = include[1] + values[i - 1]

        if include_val > exclude_val:
            # We store the updated allocation and value:
            matrix[i][j] = (include[0] + [i], include_val)
            return matrix[i][j]

        matrix[i][j] = exclude
        return matrix[i][j]

    # We first consider one (the last) item
    # and thus have full capacity:
    return explore(len(values), capacity)
