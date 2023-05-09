from ..exact import dynamic_programming_min_cost
from typing import List, Tuple


def fptas(budget: int, costs: List[int], values: List[int], accuracy: float = 0.5) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm that uses the dynamic programming algorithm to find an approximation within
    a percentage of the optimal allocation. A very good option for larger problem sizes where exact algorithms
    are too slow.

    This scales down the values to be fully polynomial in the number of projects, and thus we can say that the
    dynamic programming algorithm (which minimises costs given projects and a value) runs in fully-polynomial
    time (for these scaled down instances). The time complexity is then O(n^3/epsilon)=O(n^3/(1-accuracy)).

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :param accuracy: The precision (between 0-1) of the allocation, i.e., % of optimal solution we will accept.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)
    max_value: int = max(values)

    # The values are scaled by a factor such that they are polynomial in num_projects;
    # the rounding (casting) to int() removes precision, and thus it becomes
    # approximate:
    factor: float = epsilon * (float(max_value) / float(num_projects))
    values: List[int] = [int(float(value) / factor) for value in values]

    # The value must be scaled back up by multiplying by factor:
    result: Tuple[List[int], int] = dynamic_programming_min_cost(budget, costs, values)
    return result[0], int(float(result[1]) * factor)
