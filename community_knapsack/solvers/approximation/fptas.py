from ..exact import dynamic_programming_min_weight
from typing import List, Tuple


def fptas(capacity: int, weights: List[int], values: List[int], accuracy: float) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm that uses the dynamic programming algorithm to find an approximation within
    a percentage of the optimal allocation. A very good option for larger problem sizes where exact algorithms
    are too slow.

    This scales down the values to be fully polynomial in the number of items, and thus we can say that the
    dynamic programming algorithm (which minimises weights given items and a value) runs in fully-polynomial
    time (for these scaled down instances). The time complexity is then O(n^3/epsilon)=O(n^3/(1-accuracy)).

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :param accuracy: The precision (between 0-1) of the allocation, i.e., % of optimal solution we will accept.
    :return: The optimal allocation for the problem as a list of item indexes and its overall value.
    """
    num_items: int = len(values)
    max_value: int = max(values)

    # The accuracy value is more intuitive, but
    # we actually need 1 - accuracy to find
    # the factor:
    epsilon: float = 1 - accuracy

    # The values are scaled by a factor such that they are polynomial in num_items;
    # the rounding (casting) to int() removes precision, and thus it becomes
    # approximate:
    factor: float = epsilon * (float(max_value) / float(num_items))
    values: List[int] = [int(float(value) / factor) for value in values]

    # The value must be scaled back up by multiplying by factor:
    result: Tuple[List[int], int] = dynamic_programming_min_weight(capacity, weights, values)
    return result[0], int(float(result[1]) * factor)
