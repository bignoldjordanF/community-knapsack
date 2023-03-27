from typing import List, Tuple


def memoization(capacity, weights, values):
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result.

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
        if matrix[i][j][1] != -1:
            return matrix[i][j]

        if i == 0 or j == 0:
            matrix[i][j] = ([], 0)
            return matrix[i][j]

        if weights[i - 1] > j:
            matrix[i][j] = explore(i - 1, j)
            return matrix[i][j]

        matrix[i][j] = max(
            explore(i-1, j-weights[i-1]) + values[i-1],
            explore(i-1, j)
        )
        return matrix[i][j]

    return [], explore(len(values), capacity)
