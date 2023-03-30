from typing import List, Tuple, Any, Dict
import pulp


def integer_programming(capacity: int, weights: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A branch-and-cut integer programming solver using the PuLP library. This is typically fast,
    although it can be slow for larger pabulib.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_items: int = len(values)

    # Define an integer programming model and define a
    # binary decision variable for each item:
    model: pulp.LpProblem = pulp.LpProblem("Knapsack", pulp.LpMaximize)
    x: Dict[Any, pulp.LpVariable] = pulp.LpVariable.dicts("x", range(num_items), cat=pulp.LpBinary)

    # Define the objective function for the integer program, i.e.,
    # maximise the values of items in the allocation:
    model += pulp.lpSum([values[i] * x[i] for i in range(num_items)])

    # Define the constraint for the integer program, i.e.,
    # the weights of the items in the allocation must not
    # exceed the capacity:
    model += pulp.lpSum([weights[i] * x[i] for i in range(num_items)]) <= capacity

    # Solve the model and return the optimal allocation and value:
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    allocation: List[int] = [x[i].value() for i in range(num_items)]
    value: int = pulp.value(model.objective)
    return [idx for idx, val in enumerate(allocation) if val], value


def multi_integer_programming(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A branch-and-cut integer programming solver using the PuLP library. This is typically fast,
    although it can be slow for larger pabulib.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_items: int = len(values)

    # Define an integer programming model and define a
    # binary decision variable for each item:
    model: pulp.LpProblem = pulp.LpProblem("MDKnapsack", pulp.LpMaximize)
    x: Dict[Any, pulp.LpVariable] = pulp.LpVariable.dicts("x", range(num_items), cat=pulp.LpBinary)

    # Define the objective function for the integer program, i.e.,
    # maximise the values of items in the allocation:
    model += pulp.lpSum([values[i] * x[i] for i in range(num_items)])

    # Define the constraints for the integer program, i.e.,
    # the weights of the items must not exceed *any* of
    # the capacities:
    for j in range(len(capacities)):
        model += pulp.lpSum([weights[j][i] * x[i] for i in range(num_items)]) <= capacities[j]

    # Solve the model and return the optimal allocation and value:
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    allocation: List[int] = [x[i].value() for i in range(num_items)]
    value: int = pulp.value(model.objective)
    return [idx for idx, val in enumerate(allocation) if val], value
