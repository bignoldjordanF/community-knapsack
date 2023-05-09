from typing import List, Tuple, Union, Dict
import itertools


def dynamic_programming(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    known as bottom-up dynamic programming.

    The algorithm builds up the optimal solution by iterating through all combinations of projects and budgets. In any
    iteration (i, j), we find the maximum value possible given j budget for the first i projects by looking up the
    answer to the previous sub-problem and then either including or excluding the current project. Thus, the optimal
    solution will eventually be computed in iteration (n, C). The time complexity of the algorithm is pseudo-polynomial
    in the number of projects and budget, i.e., O(nC).

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # Store the maximum value achievable for any sub-problem:
    matrix: List[List[int]] = [
        [0 for _ in range(budget + 1)]
        for _ in range(num_projects + 1)
    ]

    # Iterate through all possible sub-problems:
    for i in range(1, num_projects + 1):
        for j in range(1, budget + 1):

            # When excluding this project, the sub-problem solution is the maximum
            # value achievable with the first i-1 projects and j budget:
            exclude: int = matrix[i - 1][j]

            if costs[i - 1] > j:
                matrix[i][j] = exclude
                continue

            # When including the project, the sub-problem solution is the maximum
            # value achievable with the first i-1 projects and j-costs[i-1]
            # budget, i.e., we must reduce the budget because we include
            # this project:
            include: int = matrix[i - 1][j - costs[i - 1]] + values[i - 1]

            # We only include the project if it can fit, otherwise we exclude it:
            if include >= exclude:
                matrix[i][j] = include
                continue

            matrix[i][j] = exclude

    best_value: int = matrix[-1][-1]
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


def dynamic_programming_min_cost(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. This is
    known as bottom-up dynamic programming.

    This variant of the dynamic programming algorithm works by finding for each iteration (i, v) the minimum cost
    achievable for an allocation containing any of the first i projects that has at least v overall value. We say v
    is in the range {1, ..., sum(values)} where sum(values) is the highest value achievable. We can then backtrack
    through our dynamic programming matrix to find the best allocation that does not exceed the budget. This runs
    in pseudo-polynomial O(n * n * P)=O(n^2 * P) time in the worst-case, where P is the maximum value (in values).

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)
    value_sum: int = sum(values)

    # Store the minimum cost achievable for any sub-problem:
    matrix: List[List[Union[int, float]]] = [
        [0 for _ in range(value_sum + 1)]
        for _ in range(num_projects + 1)
    ]

    # (Base Case 1)
    # A min. value requirement but no projects
    # is invalid -> returns infinite cost.
    for v in range(value_sum + 1):
        matrix[0][v] = float('inf')

    # (Base Case 2)
    # No min. val requirement -> just take
    # the empty allocation -> return 0.
    for i in range(num_projects + 1):
        matrix[i][0] = 0

    # Iterate through all possible sub-problems:
    for i in range(1, num_projects + 1):
        for v in range(1, value_sum + 1):

            # When excluding this project, the sub-problem solution is the minimum
            # cost achievable with the first i-1 projects achieving value v:
            exclude: Union[float, int] = matrix[i - 1][v]

            # if v < values[i - 1]:
            #     matrix[i][v] = exclude
            #     continue

            # When including this project, the sub-problem solution is the minimum
            # cost achievable with the first i-1 projects achieving value v-values[i-1],
            # i.e., the value is reduced by the current project:
            include: Union[float, int] = matrix[i - 1][v - values[i - 1]] + costs[i - 1]

            # The minimum of the costs found by including or excluding is taken
            # as the minimum cost for (i, v):
            if include < exclude:
                matrix[i][v] = include
                continue

            matrix[i][v] = exclude

    # Backtrack the matrix to find the highest value for num_projects projects at which
    # the cost does not exceed the budget:
    i: int = len(values)
    j: int = 0
    best_value: int = 0
    for v in range(sum(values), -1, -1):
        if matrix[num_projects][v] <= budget:
            best_value = v
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

    return allocation, best_value


def multi_dynamic_programming(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    An exact algorithm that improves upon the brute force algorithm, but is still extremely slow given larger
    problem sizes, especially with multiple dimensions. This is very rarely applicable.

    The algorithm builds up the optimal solution by iterating through all combinations of projects and budgets.
    Because we do not know the number of budgets, and we must iterate through {1,...budget} for each budget,
    we generate a potentially massive product of each possible loop. We calculate the maximum possible value at
    each sub-problem, and thus the result is stored in the sub-problem (num_projects, budgets). This algorithm
    runs in O(n * max(budgets)^d) time in the worst case, and cannot be better than O(n * min(budgets)^d).

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # Store the maximum value achievable for any sub-problem.
    # This approach uses a dictionary to avoid dealing with
    # a rigid d-dimensional matrix:
    memo: Dict[Tuple[int, ...], Tuple[List[int], int]] = {}

    # Generate all possible combinations of {1, ..., num_projects}
    # and {1, ..., budget} for each budget, i.e., generate
    # every possible sub-problem. This is very, very slow:
    sets: List[List[int]] = [[i for i in range(num_projects + 1)]] + \
                            [[i for i in range(budget + 1)] for budget in budgets]

    # We have to sort this *huge* list of sub-problems to consider
    # increasing budgets first for each project (simulating loops):
    sub_problems: List[Tuple[int, ...]] = sorted(list(itertools.product(*sets)))

    for sub_problem in sub_problems:
        # Split the combination into project and budgets:
        i: int = sub_problem[0]  # Current project
        j: List[int] = list(sub_problem[1:])  # Current budgets

        # We have no more projects or budget to consider,
        # so we have the empty allocation:
        if i == 0 or any(budget == 0 for budget in j):
            memo[sub_problem] = ([], 0)
            continue

        # When excluding the project, the sub-problem solution is the maximum
        # value achievable with the first i-1 projects and the same budgets:
        exclude: Tuple[List[int], int] = memo[tuple([i - 1] + j)]

        # The project must be excluded if it exceeds even one of the budgets:
        if any(costs[cid][i - 1] > budget for cid, budget in enumerate(j)):
            memo[sub_problem] = exclude
            continue

        # When including the project, the sub-problem solution is the maximum
        # value achievable with the first i-1 projects and all the budgets
        # reduced by the current cost of the project:
        include: Tuple[List[int], int] = memo[tuple(
            [i - 1] + [budget - costs[cid][i - 1] for cid, budget in enumerate(j)]
        )]
        include_val: int = include[1] + values[i - 1]

        # We only include the project if it can fit, otherwise we exclude it:
        if include_val >= exclude[1]:
            memo[sub_problem] = (include[0] + [i - 1], include_val)
            continue

        memo[sub_problem] = exclude

    # The optimal solution is stored at the sub-problem where we have
    # all the projects and all the budgets available:
    return memo[tuple([num_projects] + [budget for budget in budgets])]
