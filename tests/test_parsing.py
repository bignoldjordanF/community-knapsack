from community_knapsack import *
import os
import pytest
from typing import List


# --- Verify Parsing & Writing ---

single_tests = [
    ('resources/testing/pbfiles/example.pb', 'resources/testing/pbfiles/example_test.pb'),
]

multi_tests = [
    ('resources/testing/pbfiles/multi_example.pb', 'resources/testing/pbfiles/multi_example_test.pb')
]


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


@pytest.mark.parametrize('file_path,test_file_path', single_tests)
def test_single_parsing(file_path: str, test_file_path: str):
    """Ensures parsing a .pb file gives the correct data."""
    # Parse Pre-Existing Instance & Verify
    parser: PBParser = PBParser(file_path)
    problem: PBProblem = parser.problem()
    verify_single_example(problem)


@pytest.mark.parametrize('file_path,test_file_path', single_tests)
def test_single_writing(file_path: str, test_file_path: str):
    """Ensures writing a .pb file stores the correct data."""
    # Parse Pre-Existing Instance
    parser: PBParser = PBParser(file_path)
    problem: PBProblem = parser.problem()

    # Save Into New File
    writer: PBWriter = PBWriter(test_file_path)
    writer.write(problem)

    # Parse Again
    parser = PBParser(test_file_path)
    problem = parser.problem()

    # Verify
    verify_single_example(problem)

    # Remove Test File
    os.remove(test_file_path)


@pytest.mark.parametrize('file_path,test_file_path', multi_tests)
def test_multi_parsing(file_path: str, test_file_path: str):
    """Ensures parsing a .pb file gives the correct data."""
    # Parse Pre-Existing Instance & Verify
    parser: PBParser = PBParser(file_path)
    problem: PBMultiProblem = parser.multi_problem()
    verify_multi_example(problem)


@pytest.mark.parametrize('file_path,test_file_path', multi_tests)
def test_multi_writing(file_path: str, test_file_path: str):
    """Ensures writing a .pb file stores the correct data."""
    # Parse Pre-Existing Instance
    parser: PBParser = PBParser(file_path)
    problem: PBMultiProblem = parser.multi_problem()

    # Save Into New File
    writer: PBWriter = PBWriter(test_file_path)
    writer.write(problem)

    # Parse Again
    parser = PBParser(test_file_path)
    problem = parser.multi_problem()

    # Verify
    verify_multi_example(problem)

    # Remove Test File
    os.remove(test_file_path)


# --- Verify Allocations ---


single_test_data = [
    ('resources/testing/pbfiles/example.pb', [1, 2, 4], 7)
]
single_exact_algorithms = [
    PBAlgorithm.BRUTE_FORCE,
    PBAlgorithm.MEMOIZATION,
    PBAlgorithm.DYNAMIC_PROGRAMMING,
    PBAlgorithm.BRANCH_AND_BOUND,
    PBAlgorithm.ILP_SOLVER
]


multi_test_data = [
    ('resources/testing/pbfiles/multi_example.pb', [1, 2], 5)
]
multi_exact_algorithms = [
    PBMultiAlgorithm.BRUTE_FORCE,
    # PBMultiAlgorithm.DYNAMIC_PROGRAMMING
    PBMultiAlgorithm.MEMOIZATION,
    PBMultiAlgorithm.ILP_SOLVER
]


@pytest.mark.parametrize('file_path,allocation,value', single_test_data)
@pytest.mark.parametrize('algorithm', single_exact_algorithms)
def test_single_exact(file_path: str, allocation: List[int], value: int, algorithm: PBAlgorithm):
    """Ensures solving a .pb instance provides the correct result."""
    problem: PBProblem = PBParser(file_path).problem()
    result: PBResult = problem.solve(algorithm)
    assert result.value == value
    assert result.allocation == allocation  # Cannot always be asserted!


@pytest.mark.parametrize('file_path,allocation,value', multi_test_data)
@pytest.mark.parametrize('algorithm', multi_exact_algorithms)
def test_multi_exact(file_path: str, allocation: List[int], value: int, algorithm: PBMultiAlgorithm):
    """Ensures solving a .pb instance provides the correct result."""
    problem: PBMultiProblem = PBParser(file_path).multi_problem()
    result: PBResult = problem.solve(algorithm)
    assert result.value == value
    assert result.allocation == allocation  # Cannot always be asserted!
