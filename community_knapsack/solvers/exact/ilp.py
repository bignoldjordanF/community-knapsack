from typing import List, Tuple, Any, Dict
import pulp


def integer_programming(budget: int, costs: List[int], values: List[int]) -> Tuple[List[int], int]:
    """
    A branch-and-cut integer programming solver using the PuLP library.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # Define an integer programming model and define a
    # binary decision variable for each project:
    model: pulp.LpProblem = pulp.LpProblem("Knapsack", pulp.LpMaximize)
    x: Dict[Any, pulp.LpVariable] = pulp.LpVariable.dicts("x", range(num_projects), cat=pulp.LpBinary)

    # Define the objective function for the integer program, i.e.,
    # maximise the values of projects in the allocation:
    model += pulp.lpSum([values[i] * x[i] for i in range(num_projects)])

    # Define the constraint for the integer program, i.e.,
    # the costs of the projects in the allocation must not
    # exceed the budget:
    model += pulp.lpSum([costs[i] * x[i] for i in range(num_projects)]) <= budget

    # Solve the model and return the optimal allocation and value:
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    allocation: List[int] = [x[i].value() for i in range(num_projects)]
    value: int = pulp.value(model.objective)
    return [idx for idx, val in enumerate(allocation) if val], value


def multi_integer_programming(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int]
) -> Tuple[List[int], int]:
    """
    A branch-and-cut integer programming solver using the PuLP library.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :return: The optimal allocation for the problem as a list of project indexes and its overall value.
    """
    num_projects: int = len(values)

    # Define an integer programming model and define a
    # binary decision variable for each project:
    model: pulp.LpProblem = pulp.LpProblem("MDKnapsack", pulp.LpMaximize)
    x: Dict[Any, pulp.LpVariable] = pulp.LpVariable.dicts("x", range(num_projects), cat=pulp.LpBinary)

    # Define the objective function for the integer program, i.e.,
    # maximise the values of projects in the allocation:
    model += pulp.lpSum([values[i] * x[i] for i in range(num_projects)])

    # Define the constraints for the integer program, i.e.,
    # the costs of the projects must not exceed *any* of
    # the budgets:
    for j in range(len(budgets)):
        model += pulp.lpSum([costs[j][i] * x[i] for i in range(num_projects)]) <= budgets[j]

    # Solve the model and return the optimal allocation and value:
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    allocation: List[int] = [x[i].value() for i in range(num_projects)]
    value: int = pulp.value(model.objective)
    return [idx for idx, val in enumerate(allocation) if val], value
