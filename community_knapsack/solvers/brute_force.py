from timeit import default_timer as timer


def brute_force(capacity, weights, values):
    """
    A very slow but exact algorithm that enumerates every possible allocation and returns the optimal one.

    The allocations are enumerated by performing 2^n loops, where n is the number of items, and using the binary
    representation of each number 1,...,2^n to represent the allocation, where each bit-string of length n is unique.
    The values and weights are calculated for each allocation, and the best one is returned.

    As an indication of intractability, it takes ~0.15 seconds for n=15, ~4 seconds for n=20 and ~2 minutes for n=25.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # We track the best allocation and value throughout the iteration:
    num_items = len(values)
    best_allocation: str = '0' * num_items
    best_value: int = 0

    # Each $n$-length binary number from 1,...,n is unique -- each can represent an allocation,
    # where each bit is an item (1 = included, 0 = excluded):
    num_allocations: int = 2**num_items
    for allocation_id in range(num_allocations):

        # Convert to binary and sum weights and values of included items in the allocation:
        allocation: str = bin(allocation_id)[2:].zfill(num_items)
        value: int = sum(values[idx] for idx, bit in enumerate(allocation) if bit == '1')
        weight: int = sum(weights[idx] for idx, bit in enumerate(allocation) if bit == '1')

        # Update the best allocation found so far:
        if weight <= capacity and value > best_value:
            best_allocation = allocation
            best_value = value

    # Convert the bit-string into a list of project indexes of included items, and return:
    return [idx for idx, val in enumerate(best_allocation) if val == '1'], best_value
