from community_knapsack import *
import os
import pytest
from typing import List


single_file_path: str = 'resources/testing/pbfiles/example.pb'
single_test_file_path: str = 'resources/testing/pbfiles/example_test.pb'

multi_file_path: str = 'resources/testing/pbfiles/multi_example.pb'
multi_test_file_path: str = 'resources/testing/pbfiles/multi_example_test.pb'


def verify_single_example(problem: PBProblem):
    assert problem.num_projects == 5
    assert problem.num_voters == 5
    assert problem.budget == 10000
    assert problem.costs == [2500, 3000, 6000, 4500, 6950]
    assert problem.utilities == [
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0]
    ]


def verify_multi_example(problem: PBMultiProblem):
    assert problem.num_projects == 5
    assert problem.num_voters == 5
    assert problem.budget == [10000, 2000]
    assert problem.costs == [
        [2500, 3000, 6000, 4500, 6950],
        [1000, 700, 1250, 1500, 1750]
    ]
    assert problem.utilities == [
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0]
    ]


def test_parsing():
    # Parse Pre-Existing Instance & Verify
    parser: PBParser = PBParser(single_file_path)
    problem: PBProblem = parser.problem()
    verify_single_example(problem)


def test_writing():
    # Parse Pre-Existing Instance
    parser: PBParser = PBParser(single_file_path)
    problem: PBProblem = parser.problem()

    # Save Into New File
    writer: PBWriter = PBWriter(single_test_file_path)
    writer.write(problem)

    # Parse Again
    parser = PBParser(single_test_file_path)
    problem = parser.problem()

    # Verify
    verify_single_example(problem)

    # Remove Test File
    os.remove(single_test_file_path)


def test_multi_parsing():
    # Parse Pre-Existing Instance & Verify
    parser: PBParser = PBParser(multi_file_path)
    problem: PBMultiProblem = parser.multi_problem()
    verify_multi_example(problem)


def test_multi_writing():
    # Parse Pre-Existing Instance
    parser: PBParser = PBParser(multi_file_path)
    problem: PBMultiProblem = parser.multi_problem()

    # Save Into New File
    writer: PBWriter = PBWriter(multi_test_file_path)
    writer.write(problem)

    # Parse Again
    parser = PBParser(multi_test_file_path)
    problem = parser.multi_problem()

    # Verify
    verify_multi_example(problem)

    # Remove Test File
    os.remove(multi_test_file_path)


single_test_data = [(PBParser(single_file_path).problem(), [1, 2, 4], 7)]
single_exact_algorithms = [
    PBAlgorithm.BRUTE_FORCE,
    PBAlgorithm.MEMOIZATION,
    PBAlgorithm.DYNAMIC_PROGRAMMING,
    PBAlgorithm.BRANCH_AND_BOUND,
    PBAlgorithm.ILP_SOLVER
]


multi_test_data = [(PBParser(multi_file_path).multi_problem(), [1, 2], 5)]
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
