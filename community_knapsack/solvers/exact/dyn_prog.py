from typing import List, Tuple, Union, Dict
import itertools


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
    matrix: List[List[int]] = [
        [0 for _ in range(capacity + 1)]
        for _ in range(num_items + 1)
    ]

    # Iterate through all possible sub-problems:
    for i in range(1, num_items + 1):
        for j in range(1, capacity + 1):

            # When excluding this item, the sub-problem solution is the maximum
            # value achievable with the first i-1 items and j capacity:
            exclude: int = matrix[i - 1][j]

            if weights[i - 1] > j:
                matrix[i][j] = exclude
                continue

            # When including the item, the sub-problem solution is the maximum
            # value achievable with the first i-1 items and j-weights[i-1]
            # capacity, i.e., we must reduce the capacity because we include
            # this item:
            include: int = matrix[i - 1][j - weights[i - 1]] + values[i - 1]

            # We only include the item if it can fit, otherwise we exclude it:
            if include >= exclude:
                matrix[i][j] = include
                continue

            matrix[i][j] = exclude

    best_value: int = matrix[-1][-1]
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
    matrix: List[List[Union[int, float]]] = [
        [0 for _ in range(value_sum + 1)]
        for _ in range(num_items + 1)
    ]

    # (Base Case 1)
    # A min. value requirement but no items
    # is invalid -> returns infinite weight.
    for v in range(value_sum + 1):
        matrix[0][v] = float('inf')

    # (Base Case 2)
    # No min. val requirement -> just take
    # the empty allocation -> return 0.
    for i in range(num_items + 1):
        matrix[i][0] = 0

    # Iterate through all possible sub-problems:
    for i in range(1, num_items + 1):
        for v in range(1, value_sum + 1):

            # When excluding this item, the sub-problem solution is the minimum
            # weight achievable with the first i-1 items achieving value v:
            exclude: Union[float, int] = matrix[i - 1][v]

            # if v < values[i - 1]:
            #     matrix[i][v] = exclude
            #     continue

            # When including this item, the sub-problem solution is the minimum
            # weight achievable with the first i-1 items achieving value v-values[i-1],
            # i.e., the value is reduced by the current item:
            include: Union[float, int] = matrix[i - 1][v - values[i - 1]] + weights[i - 1]

            # The minimum of the weights found by including or excluding is taken
            # as the minimum weight for (i, v):
            if include < exclude:
                matrix[i][v] = include
                continue

            matrix[i][v] = exclude

    # Backtrack the matrix to find the highest value for num_items items at which
    # the weight does not exceed the capacity:
    i: int = len(values)
    j: int = 0
    m: int = 0
    for v in range(sum(values), -1, -1):
        if matrix[num_items][v] <= capacity:
            m = v
            j = v
            break

    # Backtrack the matrix to find an allocation
    # with `m` overall value, i.e., the highest
    # possible valid overall value:
    allocation: List[int] = []
    while i > 0 and j > 0:
        if matrix[i][j] < matrix[i - 1][j]:
            allocation.append(i - 1)
            j -= values[i - 1]
        i -= 1

    return allocation, m


def multi_dynamic_programming(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm that improves upon the brute force algorithm, but is still extremely slow given larger
    problem sizes, especially with multiple dimensions. This is very rarely applicable.

    The algorithm builds up the optimal solution by iterating through all combinations of items and capacities.
    Because we do not know the number of capacities, and we must iterate through {1,...capacity} for each capacity,
    we generate a potentially massive product of each possible loop. We calculate the maximum possible value at
    each sub-problem, and thus the result is stored in the sub-problem (num_items, capacities). This algorithm
    has worst case O(n * max(capacities)^d), and cannot be better than O(n * min(capacities)^d).

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_items: int = len(values)

    # Store the maximum value achievable for any sub-problem.
    # This approach uses a dictionary to avoid dealing with
    # a rigid d-dimensional matrix:
    memo: Dict[Tuple[int, ...], Tuple[List[int], int]] = {}

    # Generate all possible combinations of {1, ..., num_items}
    # and {1, ..., capacity} for each capacity, i.e., generate
    # every possible sub-problem. This is very, very slow:
    sets: List[List[int]] = [[i for i in range(num_items + 1)]] + \
                            [[i for i in range(capacity + 1)] for capacity in capacities]

    # We have to sort this *huge* list of sub-problems to consider
    # increasing capacities first for each item (simulating loops):
    sub_problems: List[Tuple[int, ...]] = sorted(list(itertools.product(*sets)))

    for sub_problem in sub_problems:
        # Split the combination into item and capacities:
        i: int = sub_problem[0]  # Current Item
        j: List[int] = list(sub_problem[1:])  # Current Capacities

        # We have no more items or capacity to consider,
        # so we have the empty allocation:
        if i == 0 or any(capacity == 0 for capacity in j):
            memo[sub_problem] = ([], 0)
            continue

        # When excluding the item, the sub-problem solution is the maximum
        # value achievable with the first i-1 items and the same capacities:
        exclude: Tuple[List[int], int] = memo[tuple([i - 1] + j)]

        # The item must be excluded if it exceeds even one of the capacities:
        if any(weights[cid][i - 1] > capacity for cid, capacity in enumerate(j)):
            memo[sub_problem] = exclude
            continue

        # When including the item, the sub-problem solution is the maximum
        # value achievable with the first i-1 items and all the capacities
        # reduced by the current weight of the item:
        include: Tuple[List[int], int] = memo[tuple(
            [i - 1] + [capacity - weights[cid][i - 1] for cid, capacity in enumerate(j)]
        )]
        include_val: int = include[1] + values[i - 1]

        # We only include the item if it can fit, otherwise we exclude it:
        if include_val >= exclude[1]:
            memo[sub_problem] = (include[0] + [i - 1], include_val)
            continue

        memo[sub_problem] = exclude

    # The optimal solution is stored at the sub-problem where we have
    # all the items and all the capacities available:
    return memo[tuple([num_items] + [capacity for capacity in capacities])]
