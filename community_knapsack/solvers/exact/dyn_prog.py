from typing import List, Tuple, Union


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


def dynamic_programming_min_weight(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    known as bottom-up dynamic programming.

    This variant of the dynamic programming algorithm works by finding for each iteration (i, v) the minimum weight
    achievable for an allocation containing any of the first i items that has at least v overall value. We say v
    is in the range {1, ..., sum(values)} where sum(values) is the highest value achievable. We can then backtrack
    through our dynamic programming matrix to find the best allocation that does not exceed the capacity. This runs
    in pseudo-polynomial O(n * n * P)=O(n^2 * P) time in the worst-case, where P is the maximum value (in values).

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of item indexes and its overall value.
    """
    num_items: int = len(values)
    value_sum: int = sum(values)

    # Store the minimum weight achievable for any sub-problem:
    matrix: List[List[Tuple[List[int], Union[float, int]]]] = [
        [([], 0) for _ in range(value_sum + 1)]
        for _ in range(num_items + 1)
    ]

    # (Base Case 1)
    # A min. value requirement but no items
    # is invalid -> returns infinite weight.
    for v in range(value_sum + 1):
        matrix[0][v] = ([], float('inf'))

    # (Base Case 2)
    # No min. val requirement -> just take
    # the empty allocation -> return 0.
    for i in range(num_items + 1):
        matrix[i][0] = ([], 0)

    # Iterate through all possible sub-problems:
    for i in range(1, num_items + 1):
        for v in range(1, value_sum + 1):

            # When excluding this item, the sub-problem solution is the minimum
            # weight achievable with the first i-1 items achieving value v:
            exclude: Tuple[List[int], Union[float, int]] = matrix[i - 1][v]

            # if v < values[i - 1]:
            #     matrix[i][v] = exclude
            #     continue

            # When including this item, the sub-problem solution is the minimum
            # weight achievable with the first i-1 items achieving value v-values[i-1],
            # i.e., the value is reduced by the current item:
            include: Tuple[List[int], Union[float, int]] = matrix[i - 1][v - values[i - 1]]
            include_val: int = include[1] + weights[i - 1]

            # The minimum of the weights found by including or excluding is taken
            # as the minimum weight for (i, v):
            if include_val < exclude[1]:
                matrix[i][v] = (include[0] + [i - 1], include_val)
                continue

            matrix[i][v] = exclude

    # Backtrack the matrix to find the highest
    # value for num_items items at which the
    # weight does not exceed the capacity:
    for v in range(value_sum, -1, -1):
        if matrix[num_items][v][1] <= capacity:
            return matrix[num_items][v][0], v

    return [], 0
