import pytest
from typing import List, Callable
from community_knapsack import solvers


single_instances = [
    'resources/testing/knapsack/single1.txt',
    'resources/testing/knapsack/single2.txt',
    'resources/testing/knapsack/single3.txt'
]
single_functions = [
    solvers.brute_force,
    solvers.memoization,
    solvers.dynamic_programming,
    solvers.branch_and_bound
]


@pytest.mark.parametrize('instance_file_path', single_instances)
@pytest.mark.parametrize('algorithm_fn', single_functions)
def test_single_instance(instance_file_path: str, algorithm_fn: Callable):
    with open(instance_file_path, 'r') as file:
        capacity: int = int(file.readline())
        costs: List[int] = [int(cost) for cost in file.readline().split(' ')]
        values: List[int] = [int(value) for value in file.readline().split(' ')]
        allocation: List[int] = [int(b) for b in file.readline().split(' ')]
        allocation_val: int = sum(values[idx] for idx, bit in enumerate(allocation) if bit == 1)
        assert algorithm_fn(capacity, costs, values)[1] == allocation_val


multi_instances = [
    'resources/testing/knapsack/multi1.txt',
    'resources/testing/knapsack/multi2.txt',
    # 'resources/testing/knapsack/multi3.txt'
]
multi_functions = [
    solvers.multi_brute_force,
    solvers.multi_memoization,
    # solvers.multi_dynamic_programming
]


@pytest.mark.parametrize('instance_file_path', multi_instances)
@pytest.mark.parametrize('algorithm_fn', multi_functions)
def test_multi_instance(instance_file_path: str, algorithm_fn: Callable):
    with open(instance_file_path, 'r') as file:
        n, m, v = file.readline().split(' ')
        values: List[int] = [int(value) for value in file.readline().split(' ')]
        costs: List[List[int]] = []
        for _ in range(int(m)):
            costs.append([int(cost) for cost in file.readline().split(' ')])
        budgets: List[int] = [int(budget) for budget in file.readline().split(' ')]
        assert algorithm_fn(budgets, costs, values)[1] == int(v)
