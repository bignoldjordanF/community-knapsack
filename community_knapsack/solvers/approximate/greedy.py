from typing import List, Tuple, Callable


def __greedy(
        sort_key: Callable[[Tuple[int, int, int]], float],
        capacity: int,
        weights: List[int],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    Runs the greedy algorithm on a capacity, weights and values. The algorithm
    sorts the items by the supplied sort_key and then picks the items with
    the highest (sort_key) value.

    :param sort_key: A function which decides how items should be sorted.
    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """

    # Create a list of item tuples and sort by the sort_key:
    items: List[Tuple[int, int, int]] = \
        [(pid, values[pid], weights[pid]) for pid in range(len(values))]
    items.sort(key=sort_key, reverse=True)

    allocation: List[int] = []
    value: int = 0

    for item in items:
        # Break the loop if we have
        # exhausted the capacity:
        if capacity == 0:
            break

        # Skip this item if it exceeds
        # the capacity:
        if item[2] > capacity:
            continue

        # Otherwise, include the item
        # and update the capacity:
        allocation.append(item[0])
        capacity -= item[2]
        value += item[1]

    return allocation, value


def greedy(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A fast approximation algorithm that picks items with the highest overall value. This is the most
    commonly adopted approach in practice.

    The items are sorted by their values, and then picked until either the items or capacity has
    been exhausted. Any item that cannot fit is simply skipped.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """
    # The greedy algorithm sorts items by their value:
    sort_key: Callable[[Tuple[int, int, int]], float] = \
        lambda item: item[1]

    return __greedy(sort_key, capacity, weights, values)


def ratio_greedy(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A fast and typically better (vs. greedy) approximation algorithm that picks items with the
    highest value-to-weight ratio. This is the most commonly adopted approach in practice.

    The items are sorted by their ratios, and then picked until either the items or capacity has
    been exhausted. Any item that cannot fit is simply skipped.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The allocation found for the problem as a list of project indexes and its overall value.
    """

    # The ratio-greedy algorithm sorts items by their value-to
    # weight ratio:
    sort_key: Callable[[Tuple[int, int, int]], float] = \
        lambda item: item[1] / item[2]

    return __greedy(sort_key, capacity, weights, values)


def __multi_greedy(
        sort_key: Callable[[Tuple[int, int, List[int]]], float],
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    Runs the greedy algorithm on capacities, weights and values. The algorithm
    sorts the items by the supplied sort_key and then picks the items with
    the highest (sort_key) value.

    :param sort_key: A function which decides how items should be sorted.
    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The allocation for the problem as a list of project indexes and its overall value.
    """

    # Create a list of item tuples and sort by the sort_key:
    items: List[Tuple[int, int, List[int]]] = [
        (pid, values[pid], [weights[cid][pid] for cid, _ in enumerate(capacities)])
        for pid in range(len(values))
    ]
    items.sort(key=sort_key, reverse=True)

    allocation: List[int] = []
    value: int = 0

    for item in items:
        # Break the loop if we have
        # exhausted any of the capacities:
        if any(capacity == 0 for capacity in capacities):
            break

        # Skip this item if it exceeds any
        # of the capacities:
        if any(item[2][cid] > capacity for cid, capacity in enumerate(capacities)):
            continue

        # Otherwise, include the item and update
        # the capacities:
        allocation.append(item[0])
        capacities = [capacity - item[2][cid] for cid, capacity in enumerate(capacities)]
        value += item[1]

    return allocation, value


def multi_greedy(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A fast approximation algorithm that picks items with the highest overall value.

    The items are sorted by their values, and then picked until either the items or capacities have
    been exhausted. Any item that cannot fit is simply skipped.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The allocation for the problem as a list of project indexes and its overall value.
    """

    # The multi-greedy algorithm sorts items by their value:
    sort_key: Callable[[Tuple[int, int, List[int]]], float] = \
        lambda item: item[1]

    return __multi_greedy(sort_key, capacities, weights, values)


def multi_ratio_greedy(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A fast and typically better (vs. greedy) approximation algorithm that picks items with the
    highest value-to-weight ratio. In this instance, the `weight` in the ratio is the sum of
    all weights for each item.

    The items are sorted by their ratios, and then picked until either the items or capacity has
    been exhausted. Any item that cannot fit is simply skipped.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """

    # The multi-ratio-greedy algorithm sorts items by their value-to
    # weight ratio, where `weight` is the sum of all weights for
    # each item:
    sort_key: Callable[[Tuple[int, int, List[int]]], float] = \
        lambda item: item[1] / sum(item[2])

    return __multi_greedy(sort_key, capacities, weights, values)
