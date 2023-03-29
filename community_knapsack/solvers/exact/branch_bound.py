from collections import deque
from dataclasses import dataclass
from typing import List, Tuple
from pulp import *


@dataclass
class AllocationNode:
    item: int
    """The level is the current item being considered, and is an allocation for the first {1, ..., item} items.
    In other words, it is a subset of the first {1, ..., item} items."""

    value: int
    """The overall value of this allocation."""

    weight: int
    """The overall weight of this allocation."""

    bound: float
    """The upper bound, promise or potential of this allocation, i.e., how good can this get with the other
    {item+1, ..., num_items} items?"""

    allocation: List[int]
    """A list representation of the items we have included in the allocation."""


def __bound(capacity: int, items: List[Tuple[int, int, int]], node: AllocationNode) -> float:
    """
    Given an allocation node that is a subset of the first {1, ..., node.item} items, we use the ratio greedy
    algorithm for the fractional knapsack problem to compute the potential of this node with the remaining
    {node.item + 1, ..., num_items} items.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param items: A list of item tuples (id, value, weight) sorted by value to weight ratio in non-decreasing order.
    :param node: A node representing an allocation (i.e. subset) of the first {1, ..., node.item} items.
    :return: A fractional value representing the potential value of this allocation given the remaining items.
    """
    if capacity < node.weight:
        return 0.0

    num_items: int = len(items)
    bound: float = node.value
    item: int = node.item + 1
    weight: int = node.weight

    # Add as many full items as possible until we run out of items or
    # the current item cannot fit:
    while item < num_items and weight + items[item][2] <= capacity:
        weight += items[item][2]
        bound += items[item][1]
        item += 1

    # If the capacity was insufficient, then just include
    # the highest fraction of the item possible with the
    # remaining capacity:
    if item < num_items:
        degree: float = (capacity - weight) / items[item][2]
        bound += degree * items[item][1]

    return bound


def branch_and_bound(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A relatively slow algorithm that begins to enumerate every possible allocation but prunes certain searches
    for a faster result. The run-time is exponential (slow) but can be much faster depending on the problem.

    Uses a breadth-first search approach to create a tree of allocations, where each level is an item, and we
    either decide to include or exclude it. Uses bounding and fathoms nodes to prune branches when there is
    no point exploring any further, thus improving from brute force. The worst-case time complexity is
    O(n^2), but it may perform much more efficiently.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of item indexes and its overall value.
    """
    num_items: int = len(values)

    # The items are considered by their value to weight ratio for the greedy bounding algorithm:
    items: List[Tuple[int, int, int]] = [(idx, values[idx], weights[idx]) for idx in range(num_items)]
    items.sort(key=lambda item: item[1] / item[2], reverse=True)

    # A queue for breadth-first search, i.e., constant-time pop operations:
    queue: deque[AllocationNode] = deque()
    queue.append(AllocationNode(-1, 0, 0, 0.0, []))  # Root Node

    best_allocation: List[int] = []
    best_value: int = 0

    while queue:
        # The current node represents an allocation considering `node.item` items:
        current_node: AllocationNode = queue.popleft()
        if current_node.item == num_items - 1:
            continue

        # The include node is the allocation that includes `node.item`:
        include_node: AllocationNode = AllocationNode(0, 0, 0, 0.0, [])
        include_node.item = current_node.item + 1
        include_node.value = current_node.value + items[include_node.item][1]
        include_node.weight = current_node.weight + items[include_node.item][2]
        include_node.allocation = current_node.allocation[:] + [items[include_node.item][0]]
        include_node.bound = __bound(capacity, items, include_node)  # The 'promise' or 'potential' of the allocation!

        # We update the best allocation only in the include case if it is valid:
        if include_node.weight <= capacity and include_node.value > best_value:
            best_value = include_node.value
            best_allocation = include_node.allocation

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if include_node.bound > best_value:
            queue.append(include_node)

        # The include node is the allocation that excludes `node.item`:
        exclude_node: AllocationNode = AllocationNode(0, 0, 0, 0.0, [])
        exclude_node.item = current_node.item + 1
        exclude_node.value = current_node.value
        exclude_node.weight = current_node.weight
        exclude_node.allocation = current_node.allocation[:]
        exclude_node.bound = __bound(capacity, items, exclude_node)  # The 'promise' or 'potential' of the allocation!

        # If the node has more promise or potential than our best value,
        # we do not prune the branch:
        if exclude_node.bound > best_value:
            queue.append(exclude_node)

    return best_allocation, best_value


@dataclass
class MultiAllocationNode:
    item: int
    """The level is the current item being considered, and is an allocation for the first {1, ..., item} items.
    In other words, it is a subset of the first {1, ..., item} items."""

    value: int
    """The overall value of this allocation."""

    weight: List[int]
    """The overall weight of this allocation towards each capacity."""

    bound: float
    """The upper bound, promise or potential of this allocation, i.e., how good can this get with the other
    {item+1, ..., num_items} items?"""

    allocation: List[int]
    """A list representation of the items we have included in the allocation."""


# def __lin_prog_bound(capacities, items, node):
#     if len(items) == 0 or any(node.weight[cid] > capacity for cid, capacity in enumerate(capacities)):
#         return 0.0
#
#     capacities = [capacity - node.weight[cid] for cid, capacity in enumerate(capacities)]
#     items = items[(node.item + 1):]
#
#     problem: LpProblem = LpProblem('FractionalKnapsack', LpMaximize)
#     x = [LpVariable(f'x{i}', lowBound=0, upBound=1, cat='Continuous') for i in range(len(items))]
#     problem += sum(x[i] * items[i][1] for i in range(len(items)))
#     for cid, capacity in enumerate(capacities):
#         problem += sum([x[i] * items[i][2][cid] for i in range(len(items))]) <= capacity
#     problem.solve(PULP_CBC_CMD(msg=False))
#
#     if not value(problem.objective):
#         return 0.0
#
#     return node.value + value(problem.objective)


def __multi_bound(capacities, items, node):
    if any(capacity == 0 for capacity in capacities):
        return 0.0

    if any(node.weight[cid] >= capacity for cid, capacity in enumerate(capacities)):
        return 0.0

    bound: float = node.value
    item: int = node.item + 1
    weight: List[int] = node.weight

    while item < len(items) and all(weight[cid] + items[item][2][cid] <= capacity for cid, capacity in enumerate(capacities)):
        weight = [weight[cid] + items[item][2][cid] for cid, capacity in enumerate(capacities)]
        bound += items[item][1]
        item += 1

    # Keep trying for all items and find the best bound?
    if item < len(items):
        most_exceeded: int = 0
        most_exceeded_id: int = 0
        for cid, capacity in enumerate(capacities):
            surplus: int = (weight[cid] + items[item][2][cid]) - capacity
            if surplus > most_exceeded:
                most_exceeded = surplus
                most_exceeded_id = cid
        limit: int = capacities[most_exceeded_id] - weight[most_exceeded_id]
        bound += (limit / items[item][2][most_exceeded_id]) * items[item][1]

    return bound


def multi_branch_and_bound(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """

    :param capacities:
    :param weights:
    :param values:
    :return:
    """
    num_items: int = len(values)

    items: List[Tuple[int, int, List[int]]] = \
        [(idx, values[idx], [weights[cid][idx] for cid, _ in enumerate(capacities)]) for idx in range(num_items)]
    items.sort(key=lambda item: item[1] / sum(item[2]), reverse=True)

    queue: deque[MultiAllocationNode] = deque()
    queue.append(MultiAllocationNode(-1, 0, [0] * len(capacities), 0.0, []))

    best_allocation: List[int] = []
    best_value: int = 0

    while queue:
        current_node: MultiAllocationNode = queue.popleft()
        if current_node.item == num_items - 1:
            continue

        include_node: MultiAllocationNode = MultiAllocationNode(0, 0, [0] * len(capacities), 0.0, [])
        include_node.item = current_node.item + 1
        include_node.value = current_node.value + items[include_node.item][1]
        include_node.weight = [current_node.weight[cid] + items[include_node.item][2][cid] for cid, _ in enumerate(capacities)]
        include_node.allocation = current_node.allocation[:] + [items[include_node.item][0]]
        include_node.bound = __multi_bound(capacities, items, include_node)

        if all(include_node.weight[cid] <= capacity for cid, capacity in enumerate(capacities)) and include_node.value > best_value:
            best_value = include_node.value
            best_allocation = include_node.allocation

        if include_node.bound > best_value:
            queue.append(include_node)

        exclude_node: MultiAllocationNode = MultiAllocationNode(0, 0, [0] * len(capacities), 0.0, [])
        exclude_node.item = current_node.item + 1
        exclude_node.value = current_node.value
        exclude_node.weight = current_node.weight
        exclude_node.allocation = current_node.allocation[:]
        exclude_node.bound = __multi_bound(capacities, items, exclude_node)

        if exclude_node.bound > best_value:
            queue.append(exclude_node)

    return best_allocation, best_value
