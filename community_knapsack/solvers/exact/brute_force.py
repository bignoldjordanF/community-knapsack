from typing import List, Tuple, Callable


def __brute_force(is_weight_valid: Callable[[str], bool], values: List[int]) -> Tuple[List[int], int]:
    """
    :param is_weight_valid: A function which verifies whether an allocation exceeds the capacities.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # We track the best allocation and value throughout the iteration:
    num_items = len(values)
    best_allocation: str = '0' * num_items
    best_value: int = 0

    # Each n-length binary number from 1,...,n is unique -- each can represent an allocation,
    # where each bit is an item (1 = included, 0 = excluded):
    num_allocations: int = 2**num_items
    for allocation_id in range(num_allocations):

        # Convert to binary and sum values of included items in the allocation:
        allocation: str = bin(allocation_id)[2:].zfill(num_items)
        value: int = sum(values[idx] for idx, bit in enumerate(allocation) if bit == '1')

        # Update the best allocation found so far if it does
        # not exceed the weight capacity:
        if is_weight_valid(allocation) and value > best_value:
            best_allocation = allocation
            best_value = value

    # Convert the bit-string into a list of project indexes of included items, and return:
    return [idx for idx, val in enumerate(best_allocation) if val == '1'], best_value


def brute_force(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A very slow but exact algorithm that enumerates every possible allocation and returns the optimal one.

    The allocations are enumerated by performing 2^n loops, where n is the number of items, and using the binary
    representation of each number 1,...,2^n to represent the allocation, where each bit-string of length n is unique.
    The values and weights are calculated for each allocation, and the best one is returned. This clearly takes
    O(2^n) time.

    As an indication of intractability, it takes ~0.15 seconds for n=15, ~4 seconds for n=20 and ~2 minutes for n=25.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # Checks whether an allocation is valid by summing the weights
    # of included items and checking it is less than the capacity:
    is_weight_valid: Callable[[str], bool] = lambda allocation: sum(
        weights[j] for j, bit in enumerate(allocation) if bit == '1'
    ) <= capacity

    return __brute_force(is_weight_valid, values)


def multi_brute_force(capacities: List[int], weights: List[List[int]], values: List[int]) -> Tuple[List[int], int]:
    """
    A very slow but exact algorithm that enumerates every possible allocation and returns the optimal one.

    The allocations are enumerated by performing 2^n loops, where n is the number of items, and using the binary
    representation of each number 1,...,2^n to represent the allocation, where each bit-string of length n is unique.
    The values and weights are calculated for each allocation, and the best one is returned. The time complexity
    is exponential in the number of items, i.e., O(2^n * d), where d is the number of constraints.

    As an example of intractability as the problem scales, it takes ~0.15 seconds for n=15, ~4 seconds for n=20
    and ~2 minutes for n=25.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # Checks whether an allocation is valid by summing the weights
    # of included items for each capacity and checking they are
    # less than each resource:
    is_weight_valid: Callable[[str], bool] = lambda allocation: all(
        sum(weights[i][j] for j, bit in enumerate(allocation) if bit == '1') <= capacities[i]
        for i in range(len(capacities))
    )

    return __brute_force(is_weight_valid, values)
