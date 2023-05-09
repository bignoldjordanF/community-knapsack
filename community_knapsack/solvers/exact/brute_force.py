from typing import List, Tuple, Callable


def __brute_force(is_cost_valid: Callable[[str], bool], values: List[int]) -> Tuple[List[int], int]:
    """
    :param is_cost_valid: A function which verifies whether an allocation exceeds the budgets.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # We track the best allocation and value throughout the iteration:
    num_projects = len(values)
    best_allocation: str = '0' * num_projects
    best_value: int = 0

    # Each n-length binary number from 1,...,n is unique -- each can represent an allocation,
    # where each bit is a project (1 = included, 0 = excluded):
    num_allocations: int = 2**num_projects
    for allocation_id in range(num_allocations):

        # Convert to binary and sum values of included projects in the allocation:
        allocation: str = bin(allocation_id)[2:].zfill(num_projects)
        value: int = sum(values[idx] for idx, bit in enumerate(allocation) if bit == '1')

        # Update the best allocation found so far if it does
        # not exceed the cost budget:
        if is_cost_valid(allocation) and value > best_value:
            best_allocation = allocation
            best_value = value

    # Convert the bit-string into a list of project indexes of included projects, and return:
    return [idx for idx, val in enumerate(best_allocation) if val == '1'], best_value


def brute_force(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A very slow but exact algorithm that enumerates every possible allocation and returns the optimal one.

    The allocations are enumerated by performing 2^n loops, where n is the number of projects, and using the binary
    representation of each number 1,...,2^n to represent the allocation, where each bit-string of length n is unique.
    The values and costs are calculated for each allocation, and the best one is returned. This clearly takes
    O(2^n) time.

    As an indication of intractability, it takes ~0.15 seconds for n=15, ~4 seconds for n=20 and ~2 minutes for n=25.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # Checks whether an allocation is valid by summing the costs
    # of included projects and checking it is less than the budget:
    is_cost_valid: Callable[[str], bool] = lambda allocation: sum(
        costs[j] for j, bit in enumerate(allocation) if bit == '1'
    ) <= budget

    return __brute_force(is_cost_valid, values)


def multi_brute_force(budgets: List[int], costs: List[List[int]], values: List[int]) -> Tuple[List[int], int]:
    """
    A very slow but exact algorithm that enumerates every possible allocation and returns the optimal one.

    The allocations are enumerated by performing 2^n loops, where n is the number of projects, and using the binary
    representation of each number 1,...,2^n to represent the allocation, where each bit-string of length n is unique.
    The values and costs are calculated for each allocation, and the best one is returned. The time complexity
    is exponential in the number of projects, i.e., O(2^n * d), where d is the number of constraints.

    As an example of intractability as the problem scales, it takes ~0.15 seconds for n=15, ~4 seconds for n=20
    and ~2 minutes for n=25.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    # Checks whether an allocation is valid by summing the costs
    # of included projects for each budget and checking they are
    # less than each resource:
    is_cost_valid: Callable[[str], bool] = lambda allocation: all(
        sum(costs[i][j] for j, bit in enumerate(allocation) if bit == '1') <= budgets[i]
        for i in range(len(budgets))
    )

    return __brute_force(is_cost_valid, values)
