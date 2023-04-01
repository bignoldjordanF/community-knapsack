import pytest
from typing import List, Callable
from community_knapsack import solvers


instances = [
    'resources/testing/knapsack/multi1.txt',
    'resources/testing/knapsack/multi2.txt',
    'resources/testing/knapsack/multi3.txt'
]

functions = [
    solvers.multi_brute_force,
    solvers.multi_memoization,
    # solvers.multi_dynamic_programming
]


@pytest.mark.parametrize('instance_file_path', instances)
@pytest.mark.parametrize('algorithm_fn', functions)
def test_instance(instance_file_path: str, algorithm_fn: Callable):
    with open(instance_file_path, 'r') as file:
        n, m, v = file.readline().split(' ')
        values: List[int] = [int(value) for value in file.readline().split(' ')]
        costs: List[List[int]] = []
        for _ in range(int(m)):
            costs.append([int(cost) for cost in file.readline().split(' ')])
        budgets: List[int] = [int(budget) for budget in file.readline().split(' ')]
        assert algorithm_fn(budgets, costs, values)[1] == int(v)
