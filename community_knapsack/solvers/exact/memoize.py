from typing import List, Tuple, Dict


def memoization(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    also known as top-down dynamic programming.

    The algorithm explores all possible allocations through branches in a recursion tree, i.e., we create two
    branches: one that includes the current project and one that does not. We store the results of branches that have
    already been explored thus avoiding re-computation and upper bounding the time complexity of the algorithm to
    be pseudo-polynomial in the number of projects and budget, i.e., O(nC).

    :param budget: The fixed budget or budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # Store the maximum value achievable for any sub-problem:
    matrix: List[List[int]] = [
        [-1 for _ in range(budget + 1)]
        for _ in range(num_projects + 1)
    ]

    def explore(i: int, j: int) -> int:
        # Avoid re-computation through
        # memoization:
        if matrix[i][j] != -1:
            return matrix[i][j]

        # (Base Case)
        # We have no more projects or
        # budget to consider:
        if i == 0 or j == 0:
            matrix[i][j] = 0
            return matrix[i][j]

        # (Recursive Case 1)
        # We cannot fit the current
        # project, so we must exclude:
        if costs[i - 1] > j:
            matrix[i][j] = explore(i - 1, j)
            return matrix[i][j]

        # (Recursive Case 2)
        # Include the current project if
        # and only if it leads to a
        # larger value than excluding:
        exclude: int = explore(i - 1, j)
        include: int = explore(i - 1, j - costs[i - 1]) + values[i - 1]

        if include > exclude:
            # We store the updated allocation and value:
            matrix[i][j] = include
            return matrix[i][j]

        matrix[i][j] = exclude
        return matrix[i][j]

    # We first consider one (the last) project
    # and have full budget:
    best_value: int = explore(num_projects, budget)
    allocation: List[int] = []

    # Backtrack the matrix to find an allocation
    # with `best_value` overall value:
    i: int = num_projects
    j: int = budget
    while i > 0 and j > 0:
        if matrix[i][j] != matrix[i - 1][j]:
            allocation.append(i - 1)
            j -= costs[i - 1]
        i -= 1

    return allocation, best_value


def multi_memoization(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm that improves upon the brute force algorithm for a faster result. This is also known as a
    top-down dynamic programming approach.

    The algorithm explores all possible allocations through branches in a recursion tree, i.e., we create two
    branches: one that includes the current project and one that does not. We store the results of branches that have
    already been explored thus avoiding re-computation. In the worst case, we explore every possible project and every
    possible budget, and thus the time complexity is O(n * max(budgets)^d), where d is the number of budgets,
    in the worst case.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

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
        # We have no more projects or budget to consider:
        if i == 0 or any(budget == 0 for budget in j):
            memo[sub_problem] = ([], 0)
            return memo[sub_problem]

        # (Recursive Case 1)
        # We cannot fit the current project, so we must exclude:
        if any(costs[cid][i - 1] > budget for cid, budget in enumerate(j)):
            memo[sub_problem] = explore(i - 1, j)
            return memo[sub_problem]

        # (Recursive Case 2)
        # Find the maximum values from including and excluding. We must update
        # the budget list to reflect including the project:
        j_updated: List[int] = [budget - costs[cid][i - 1] for cid, budget in enumerate(j)]
        include: Tuple[List[int], int] = explore(i - 1, j_updated)
        exclude: Tuple[List[int], int] = explore(i - 1, j)

        # Accept the allocation that includes the current project if and only if
        # it has a higher overall value, otherwise accept the exclusion:
        if include[1] + values[i - 1] > exclude[1]:
            memo[sub_problem] = (include[0] + [i - 1], include[1] + values[i - 1])
            return memo[sub_problem]

        memo[sub_problem] = exclude
        return memo[sub_problem]

    # We first consider one (the last) project
    # and have full budget:
    return explore(num_projects, budgets)
