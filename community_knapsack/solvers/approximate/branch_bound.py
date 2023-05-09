from collections import deque
from dataclasses import dataclass
from typing import List, Tuple
# from pulp import *


@dataclass
class MultiAllocationNode:
    project: int
    """The level is the current project being considered, and is an allocation for the first {1, ..., project} projects.
    In other words, it is a subset of the first {1, ..., project} projects."""

    value: int
    """The overall value of this allocation."""

    cost: List[int]
    """The overall cost of this allocation towards each budget."""

    bound: float
    """The upper bound, promise or potential of this allocation, i.e., how good can this get with the other
    {project+1, ..., num_projects} projects?"""

    allocation: List[int]
    """A list representation of the projects we have included in the allocation."""


# def __lin_prog_bound(budgets, projects, node):
#     if len(projects) == 0 or any(node.cost[cid] > budget for cid, budget in enumerate(budgets)):
#         return 0.0
#
#     budgets = [budget - node.cost[cid] for cid, budget in enumerate(budgets)]
#     projects = projects[(node.project + 1):]
#
#     problem: LpProblem = LpProblem('FractionalKnapsack', LpMaximize)
#     x = [LpVariable(f'x{i}', lowBound=0, upBound=1, cat='Continuous') for i in range(len(projects))]
#     problem += sum(x[i] * projects[i][1] for i in range(len(projects)))
#     for cid, budget in enumerate(budgets):
#         problem += sum([x[i] * projects[i][2][cid] for i in range(len(projects))]) <= budget
#     problem.solve(PULP_CBC_CMD(msg=False))
#
#     if not value(problem.objective):
#         return 0.0
#
#     return node.value + value(problem.objective)


def __multi_bound(budgets, projects, node):
    """
    Given an allocation node that is a subset of the first {1, ..., node.project} projects, we use the ratio greedy
    algorithm for the fractional multidimensional knapsack problem to approximate the upper bound or potential
    of this node with the remaining projects {node.project + 1, ..., num_projects} projects. This algorithm does *not*
    exactly solve the problem and is an approximation.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed this number.
    :param projects: A list of project tuples (id, value, cost) sorted by value to cost ratio in non-decreasing order.
    :param node: A node representing an allocation (i.e. subset) of the first {1, ..., node.project} projects.
    :return: A fractional value representing the potential value of this allocation given the remaining projects.
    """

    # If there is no budget then we want to prune this branch, so give it a
    # zero bound:
    if any(budget <= node.cost[cid] for cid, budget in enumerate(budgets)):
        return 0.0

    bound: float = node.value
    project: int = node.project + 1
    cost: List[int] = node.cost

    # Add as many full projects as possible until we run out of projects or the current project cannot fit:
    while project < len(projects) and \
            all(cost[cid] + projects[project][2][cid] <= budget for cid, budget in enumerate(budgets)):
        cost = [cost[cid] + projects[project][2][cid] for cid, budget in enumerate(budgets)]
        bound += projects[project][1]
        project += 1

    # If the budgets were insufficient, then include the highest fraction of the project
    # possible with the remaining budgets:
    if project < len(projects):
        # In simple terms, take the budget with the smallest 'wiggle room' and then
        # fill that budget as much as possible:
        fraction: float = float('inf')
        for cid, budget in enumerate(budgets):
            diff: int = budget - cost[cid]  # Amount of 'wiggle room'
            fraction: float = min(fraction, diff / projects[project][2][cid])  # Fraction of project
        if fraction == float('inf'):
            fraction = 0.0
        bound += fraction * projects[project][1]  # Update upper value bound

    return bound


def multi_branch_and_bound(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    An approximation algorithm that begins to enumerate every possible allocation but prunes
    certain branches for a faster result. The run-time is exponential (slow) but can be much
    faster depending on the problem.

    Uses a breadth-first search approach to create a tree of allocations, where each level is an project,
    and we either decide to include or exclude it. Uses an approximation algorithm (ratio greedy) to
    bound and fathom nodes to prune branches when there is no point exploring further. This improves
    from brute force but can lead to inaccuracies due to the bounding approximation. The worst-case
    time complexity is O(n^2 * d), where d is the number of constraints, but it may perform much
    more efficiently.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # The projects are considered by their value to cost ratio for the greedy bounding algorithm:
    projects: List[Tuple[int, int, List[int]]] = \
        [(idx, values[idx], [costs[cid][idx] for cid, _ in enumerate(budgets)]) for idx in range(num_projects)]
    projects.sort(key=lambda project: project[1] / sum(project[2]), reverse=True)

    # A queue for breadth-first search, i.e., for constant-time pop operations:
    queue: deque[MultiAllocationNode] = deque()
    queue.append(MultiAllocationNode(-1, 0, [0] * len(budgets), 0.0, []))  # Root Node

    best_allocation: List[int] = []
    best_value: int = 0

    while queue:
        # The current node represents an allocation considering `node.project` projects:
        current_node: MultiAllocationNode = queue.popleft()
        if current_node.project == num_projects - 1:
            continue

        # The include node is the allocation that includes `node.project`:
        include_node: MultiAllocationNode = MultiAllocationNode(0, 0, [0] * len(budgets), 0.0, [])
        include_node.project = current_node.project + 1
        include_node.value = current_node.value + projects[include_node.project][1]
        include_node.cost = [
            current_node.cost[cid] + projects[include_node.project][2][cid] for cid, _ in enumerate(budgets)
        ]
        include_node.allocation = current_node.allocation[:] + [projects[include_node.project][0]]
        include_node.bound = __multi_bound(budgets, projects, include_node)

        # We only update the best allocation in the include case, and it must be valid:
        if include_node.value > best_value and \
                all(include_node.cost[cid] <= budget for cid, budget in enumerate(budgets)):
            best_value = include_node.value
            best_allocation = include_node.allocation

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if include_node.bound > best_value:
            queue.append(include_node)

        # The exclude node is the allocation that excludes `node.project`:
        exclude_node: MultiAllocationNode = MultiAllocationNode(0, 0, [0] * len(budgets), 0.0, [])
        exclude_node.project = current_node.project + 1
        exclude_node.value = current_node.value
        exclude_node.cost = current_node.cost
        exclude_node.allocation = current_node.allocation[:]
        exclude_node.bound = __multi_bound(budgets, projects, exclude_node)

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if exclude_node.bound > best_value:
            queue.append(exclude_node)

    return best_allocation, best_value
