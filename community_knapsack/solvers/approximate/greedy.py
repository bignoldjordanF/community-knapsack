from typing import List, Tuple, Callable


def __greedy(
        sort_key: Callable[[Tuple[int, int, int]], float],
        budget: int,
        costs: List[int],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    Runs the greedy algorithm on a budget, costs and values. The algorithm
    sorts the projects by the supplied sort_key and then picks the projects with
    the highest (sort_key) value.

    :param sort_key: A function which decides how projects should be sorted.
    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """

    # Create a list of project tuples and sort by the sort_key:
    projects: List[Tuple[int, int, int]] = \
        [(pid, values[pid], costs[pid]) for pid in range(len(values))]
    projects.sort(key=sort_key, reverse=True)

    allocation: List[int] = []
    value: int = 0

    for project in projects:
        # Break the loop if we have
        # exhausted the budget:
        if budget == 0:
            break

        # Skip this project if it exceeds
        # the budget:
        if project[2] > budget:
            continue

        # Otherwise, include the project
        # and update the budget:
        allocation.append(project[0])
        budget -= project[2]
        value += project[1]

    return allocation, value


def greedy(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A fast approximation algorithm that picks projects with the highest overall value. This is the most
    commonly adopted approach in practice.

    The projects are sorted by their values, and then picked until either the projects or budget has
    been exhausted. Any project that cannot fit is simply skipped.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """
    # The greedy algorithm sorts projects by their value:
    sort_key: Callable[[Tuple[int, int, int]], float] = \
        lambda project: project[1]

    return __greedy(sort_key, budget, costs, values)


def ratio_greedy(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A fast and typically better (vs. greedy) approximation algorithm that picks projects with the
    highest value-to-cost ratio. This is the most commonly adopted approach in practice.

    The projects are sorted by their ratios, and then picked until either the projects or budget has
    been exhausted. Any project that cannot fit is simply skipped.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """

    # The ratio-greedy algorithm sorts projects by their value-to
    # cost ratio:
    sort_key: Callable[[Tuple[int, int, int]], float] = \
        lambda project: project[1] / project[2]

    return __greedy(sort_key, budget, costs, values)


def __multi_greedy(
        sort_key: Callable[[Tuple[int, int, List[int]]], float],
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    Runs the greedy algorithm on budgets, costs and values. The algorithm
    sorts the projects by the supplied sort_key and then picks the projects with
    the highest (sort_key) value.

    :param sort_key: A function which decides how projects should be sorted.
    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation for the problem as a list of project indexes and its overall value.
    """

    # Create a list of project tuples and sort by the sort_key:
    projects: List[Tuple[int, int, List[int]]] = [
        (pid, values[pid], [costs[cid][pid] for cid, _ in enumerate(budgets)])
        for pid in range(len(values))
    ]
    projects.sort(key=sort_key, reverse=True)

    allocation: List[int] = []
    value: int = 0

    for project in projects:
        # Break the loop if we have
        # exhausted any of the budgets:
        if any(budget == 0 for budget in budgets):
            break

        # Skip this project if it exceeds any
        # of the budgets:
        if any(project[2][cid] > budget for cid, budget in enumerate(budgets)):
            continue

        # Otherwise, include the project and update
        # the budgets:
        allocation.append(project[0])
        budgets = [budget - project[2][cid] for cid, budget in enumerate(budgets)]
        value += project[1]

    return allocation, value


def multi_greedy(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A fast approximation algorithm that picks projects with the highest overall value.

    The projects are sorted by their values, and then picked until either the projects or budgets have
    been exhausted. Any project that cannot fit is simply skipped.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation for the problem as a list of project indexes and its overall value.
    """

    # The multi-greedy algorithm sorts projects by their value:
    sort_key: Callable[[Tuple[int, int, List[int]]], float] = \
        lambda project: project[1]

    return __multi_greedy(sort_key, budgets, costs, values)


def multi_ratio_greedy(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A fast and typically better (vs. greedy) approximation algorithm that picks projects with the
    highest value-to-cost ratio. In this instance, the `cost` in the ratio is the sum of
    all costs for each project.

    The projects are sorted by their ratios, and then picked until either the projects or budget has
    been exhausted. Any project that cannot fit is simply skipped.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """

    # The multi-ratio-greedy algorithm sorts projects by their value-to
    # cost ratio, where `cost` is the sum of all costs for
    # each project:
    sort_key: Callable[[Tuple[int, int, List[int]]], float] = \
        lambda project: project[1] / sum(project[2])

    return __multi_greedy(sort_key, budgets, costs, values)
