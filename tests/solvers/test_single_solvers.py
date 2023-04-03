from community_knapsack import solvers
from typing import List, Callable
import pytest


class TestClassicKnapsack:
    """Ensures the solver algorithms for the classic knapsack problem produce correct and/or reasonable results."""

    knapsack_test_file_paths: List[str] = [
        'resources/tests/knapsack/single/p01.txt',
        'resources/tests/knapsack/single/p02.txt',
        'resources/tests/knapsack/single/p03.txt',
        'resources/tests/knapsack/single/p04.txt',
        'resources/tests/knapsack/single/p05.txt',
        'resources/tests/knapsack/single/p06.txt',
        'resources/tests/knapsack/single/p07.txt'
        # 'resources/tests/single/p08.txt',  # passes but is very slow!
    ]

    exact_solver_functions: List[Callable] = [
        solvers.exact.brute_force,
        solvers.exact.memoization,
        solvers.exact.dynamic_programming,
        solvers.exact.branch_and_bound,
        solvers.exact.integer_programming
    ]

    approximate_solver_functions: List[Callable] = [
        solvers.approximate.fptas,
        solvers.approximate.simulated_annealing,
        solvers.approximate.genetic_algorithm,
        solvers.approximate.ratio_greedy
    ]

    @staticmethod
    def _parse_file(file_path: str):
        with open(file_path, 'r') as data:
            # Extract the knapsack test data from the test files:
            capacity: int = int(data.readline())
            weights: List[int] = [int(weight.strip()) for weight in data.readline().split(' ')]
            values: List[int] = [int(value.strip()) for value in data.readline().split(' ')]
            optimal: int = int(data.readline().strip())
            return capacity, weights, values, optimal

    @pytest.mark.parametrize('file_path', knapsack_test_file_paths)
    @pytest.mark.parametrize('solver', exact_solver_functions)
    def test_exact_solvers(self, file_path: str, solver: Callable):
        # Parse each file and ensure the solver gives the optimal value:
        capacity, weights, values, optimal = TestClassicKnapsack._parse_file(file_path)
        assert solver(capacity, weights, values)[1] == optimal

    @pytest.mark.parametrize('file_path', knapsack_test_file_paths)
    @pytest.mark.parametrize('solver', approximate_solver_functions)
    def test_approximate_solvers(self, file_path: str, solver: Callable):
        # Parse each file and ensure the solver gives a value
        # within 30% of the optimal value. This is not guaranteed for
        # every instance, but shows that the approximations genuinely
        # converge on optima for each instance:
        capacity, weights, values, optimal = TestClassicKnapsack._parse_file(file_path)
        assert abs(solver(capacity, weights, values)[1] - optimal) <= (0.3 * optimal)
