from community_knapsack import *
import pytest


single_test_data = [PBParser('resources/demonstration/example.pb').problem()]
single_exact_algorithms = [
    PBAlgorithm.BRUTE_FORCE,
    PBAlgorithm.MEMOIZATION,
    PBAlgorithm.DYNAMIC_PROGRAMMING,
    PBAlgorithm.BRANCH_AND_BOUND,
    PBAlgorithm.ILP_SOLVER
]


multi_test_data = [PBParser('resources/demonstration/multi_example.pb').multi_problem()]
multi_exact_algorithms = [
    PBMultiAlgorithm.BRUTE_FORCE,
    # PBMultiAlgorithm.DYNAMIC_PROGRAMMING
    PBMultiAlgorithm.MEMOIZATION,
    PBMultiAlgorithm.ILP_SOLVER
]


@pytest.mark.parametrize('problem', single_test_data)
@pytest.mark.parametrize('algorithm', single_exact_algorithms)
def test_single_exact(problem: PBProblem, algorithm: PBAlgorithm):

    result: PBResult = problem.solve(algorithm)
    assert result.value == 7
    assert result.allocation == [1, 2, 4]  # Cannot always be asserted!


@pytest.mark.parametrize('problem', multi_test_data)
@pytest.mark.parametrize('algorithm', multi_exact_algorithms)
def test_multi_exact(problem: PBMultiProblem, algorithm: PBMultiAlgorithm):

    result: PBResult = problem.solve(algorithm)
    assert result.value == 5
    assert result.allocation == [1, 2]  # Cannot always be asserted!
