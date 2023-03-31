from typing import List
from community_knapsack import *
import pytest


single_test_data = [(PBParser('resources/demonstration/example.pb').problem(), [1, 2, 4], 7)]
single_exact_algorithms = [
    PBAlgorithm.BRUTE_FORCE,
    PBAlgorithm.MEMOIZATION,
    PBAlgorithm.DYNAMIC_PROGRAMMING,
    PBAlgorithm.BRANCH_AND_BOUND,
    PBAlgorithm.ILP_SOLVER
]


multi_test_data = [(PBParser('resources/demonstration/multi_example.pb').multi_problem(), [1, 2], 5)]
multi_exact_algorithms = [
    PBMultiAlgorithm.BRUTE_FORCE,
    # PBMultiAlgorithm.DYNAMIC_PROGRAMMING
    PBMultiAlgorithm.MEMOIZATION,
    PBMultiAlgorithm.ILP_SOLVER
]


@pytest.mark.parametrize('problem,allocation,value', single_test_data)
@pytest.mark.parametrize('algorithm', single_exact_algorithms)
def test_single_exact(problem: PBProblem, allocation: List[int], value: int, algorithm: PBAlgorithm):

    result: PBResult = problem.solve(algorithm)
    assert result.value == value
    assert result.allocation == allocation  # Cannot always be asserted!


@pytest.mark.parametrize('problem,allocation,value', multi_test_data)
@pytest.mark.parametrize('algorithm', multi_exact_algorithms)
def test_multi_exact(problem: PBMultiProblem, allocation: List[int], value: int, algorithm: PBMultiAlgorithm):

    result: PBResult = problem.solve(algorithm)
    assert result.value == value
    assert result.allocation == allocation  # Cannot always be asserted!
