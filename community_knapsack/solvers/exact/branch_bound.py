from collections import deque
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class AllocationNode:
    project: int
    """The level is the current project being considered, and is an allocation for the first {1, ..., project} projects.
    In other words, it is a subset of the first {1, ..., project} projects."""

    value: int
    """The overall value of this allocation."""

    cost: int
    """The overall cost of this allocation."""

    bound: float
    """The upper bound, promise or potential of this allocation, i.e., how good can this get with the other
    {project+1, ..., num_projects} projects?"""

    allocation: List[int]
    """A list representation of the projects we have included in the allocation."""


def __bound(budget: int, projects: List[Tuple[int, int, int]], node: AllocationNode) -> float:
    """
    Given an allocation node that is a subset of the first {1, ..., node.project} projects, we use the ratio greedy
    algorithm for the fractional knapsack problem to compute the potential of this node with the remaining
    {node.project + 1, ..., num_projects} projects.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param projects: A list of project tuples (id, value, cost) sorted by value to cost ratio in non-decreasing order.
    :param node: A node representing an allocation (i.e. subset) of the first {1, ..., node.project} projects.
    :return: A fractional value representing the potential value of this allocation given the remaining projects.
    """
    if budget < node.cost:
        return 0.0

    num_projects: int = len(projects)
    bound: float = node.value
    project: int = node.project + 1
    cost: int = node.cost

    # Add as many full projects as possible until we run out of projects or
    # the current project cannot fit:
    while project < num_projects and cost + projects[project][2] <= budget:
        cost += projects[project][2]
        bound += projects[project][1]
        project += 1

    # If the budget was insufficient, then just include
    # the highest fraction of the project possible with the
    # remaining budget:
    if project < num_projects:
        degree: float = (budget - cost) / projects[project][2]
        bound += degree * projects[project][1]

    return bound


def branch_and_bound(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    An exact algorithm that begins to enumerate every possible allocation but prunes certain branches
    for a faster result. The run-time is exponential (slow) but can be much faster depending on the
    problem.

    Uses a breadth-first search approach to create a tree of allocations, where each level is a project, and we
    either decide to include or exclude it. Uses bounding and fathoms nodes to prune branches when there is
    no point exploring any further, thus improving from brute force. The worst-case time complexity is
    O(n^2), but it may perform much more efficiently.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # The projects are considered by their value to cost ratio for the greedy bounding algorithm:
    projects: List[Tuple[int, int, int]] = [(idx, values[idx], costs[idx]) for idx in range(num_projects)]
    projects.sort(key=lambda project: project[1] / project[2], reverse=True)

    # A queue for breadth-first search, i.e., for constant-time pop operations:
    queue: deque[AllocationNode] = deque()
    queue.append(AllocationNode(-1, 0, 0, 0.0, []))  # Root Node

    best_allocation: List[int] = []
    best_value: int = 0

    while queue:
        # The current node represents an allocation considering `node.project` projects:
        current_node: AllocationNode = queue.popleft()
        if current_node.project == num_projects - 1:
            continue

        # The include node is the allocation that includes `node.project`:
        include_node: AllocationNode = AllocationNode(0, 0, 0, 0.0, [])
        include_node.project = current_node.project + 1
        include_node.value = current_node.value + projects[include_node.project][1]
        include_node.cost = current_node.cost + projects[include_node.project][2]
        include_node.allocation = current_node.allocation[:] + [projects[include_node.project][0]]
        include_node.bound = __bound(budget, projects, include_node)  # The 'promise' or 'potential' of the allocation!

        # We update the best allocation only in the include case if it is valid:
        if include_node.cost <= budget and include_node.value > best_value:
            best_value = include_node.value
            best_allocation = include_node.allocation

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if include_node.bound > best_value:
            queue.append(include_node)

        # The exclude node is the allocation that excludes `node.project`:
        exclude_node: AllocationNode = AllocationNode(0, 0, 0, 0.0, [])
        exclude_node.project = current_node.project + 1
        exclude_node.value = current_node.value
        exclude_node.cost = current_node.cost
        exclude_node.allocation = current_node.allocation[:]
        exclude_node.bound = __bound(budget, projects, exclude_node)  # The 'promise' or 'potential' of the allocation!

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if exclude_node.bound > best_value:
            queue.append(exclude_node)

    return best_allocation, best_value
