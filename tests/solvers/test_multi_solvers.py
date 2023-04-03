from community_knapsack import solvers
from typing import List, Callable
import pytest


class TestMultiDimensionalKnapsack:
    """Ensures the solver algorithms for the multidimensional knapsack problem produce correct and/or reasonable
    results."""

    knapsack_test_file_paths: List[str] = [
        'resources/tests/knapsack/multi/p01.txt',
        'resources/tests/knapsack/multi/p02.txt',
        'resources/tests/knapsack/multi/p03.txt',
        'resources/tests/knapsack/multi/p04.txt',
        'resources/tests/knapsack/multi/p05.txt',
    ]

    exact_solver_functions: List[Callable] = [
        solvers.exact.multi_brute_force,
        solvers.exact.multi_memoization,
        solvers.exact.multi_integer_programming
    ]

    approximate_solver_functions: List[Callable] = [
        solvers.approximate.multi_branch_and_bound,
        solvers.approximate.multi_simulated_annealing,
        solvers.approximate.multi_genetic_algorithm,
        solvers.approximate.multi_ratio_greedy
    ]

    @staticmethod
    def _parse_file(file_path: str):
        with open(file_path, 'r') as data:
            # Extract the knapsack test data from the test files:
            capacities: List[int] = [int(capacity) for capacity in data.readline().split(' ')]

            weights: List[List[int]] = []
            for _ in range(len(capacities)):
                weights.append([int(weight) for weight in data.readline().split(' ')])

            values: List[int] = [int(value.strip()) for value in data.readline().split(' ')]
            optimal: int = int(data.readline().strip())
            return capacities, weights, values, optimal

    @pytest.mark.parametrize('file_path', knapsack_test_file_paths)
    @pytest.mark.parametrize('solver', exact_solver_functions)
    def test_exact_solvers(self, file_path: str, solver: Callable):
        # Parse each file and ensure the solver gives the optimal value:
        capacities, weights, values, optimal = TestMultiDimensionalKnapsack._parse_file(file_path)
        assert solver(capacities, weights, values)[1] == optimal

    @pytest.mark.parametrize('file_path', knapsack_test_file_paths)
    @pytest.mark.parametrize('solver', approximate_solver_functions)
    def test_approximate_solvers(self, file_path: str, solver: Callable):
        # Parse each file and ensure the solver gives a value
        # within 30% of the optimal value. This is not guaranteed for
        # every instance, but shows that the approximations genuinely
        # converge on optima for each instance:
        capacity, weights, values, optimal = TestMultiDimensionalKnapsack._parse_file(file_path)
        assert abs(solver(capacity, weights, values)[1] - optimal) <= (0.3 * optimal)
