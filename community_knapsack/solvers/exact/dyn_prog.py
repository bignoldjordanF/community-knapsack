from typing import List, Tuple


def dynamic_programming(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    known as bottom-up dynamic programming.

    The algorithm builds up the optimal solution by iterating through all combinations of items and capacities. In any
    iteration (i, j), we find the maximum value possible given j capacity for the first i items by looking up the
    answer to the previous sub-problem and then either including or excluding the current item. Thus, the optimal
    solution will eventually be computed in iteration (n, C). The time complexity of the algorithm is pseudo-polynomial
    in the number of items and capacity, i.e., O(nC).

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of item indexes and its overall value.
    """
    num_items: int = len(values)

    # Store the maximum value achievable for any sub-problem:
    matrix: List[List[Tuple[List[int], int]]] = [
        [([], 0) for _ in range(capacity + 1)]
        for _ in range(num_items + 1)
    ]

    # Iterate through all possible sub-problems:
    for i in range(1, num_items + 1):
        for j in range(1, capacity + 1):

            # When excluding this item, the sub-problem solution is the maximum
            # value achievable with the first i-1 items and j capacity:
            exclude: Tuple[List[int], int] = matrix[i - 1][j]

            if weights[i - 1] > j:
                matrix[i][j] = exclude
                continue

            # When including the item, the sub-problem solution is the maximum
            # value achievable with the first i-1 items and j-weights[i-1]
            # capacity, i.e., we must reduce the capacity because we include
            # this item:
            include: Tuple[List[int], int] = matrix[i - 1][j - weights[i - 1]]
            include_val: int = include[1] + values[i - 1]

            # We only include the item if it can fit, otherwise we exclude it:
            if include_val >= exclude[1]:
                matrix[i][j] = (include[0] + [i - 1], include_val)
                continue

            matrix[i][j] = exclude

    return matrix[-1][-1]
