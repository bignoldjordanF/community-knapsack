from community_knapsack import *
import os


single_file_path: str = 'resources/demonstration/example.pb'
single_test_file_path: str = 'resources/demonstration/example_test.pb'

multi_file_path: str = 'resources/demonstration/multi_example.pb'
multi_test_file_path: str = 'resources/demonstration/multi_example_test.pb'


def verify_single_example(problem: PBProblem):
    assert problem.num_projects == 5
    assert problem.num_voters == 5
    assert problem.budget == 1000
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
    assert problem.budget == [1000, 2000]
    assert problem.costs == [
        [2500, 3000, 6000, 4500, 6950],
        [1000, 700, 1250, 500, 1750]
    ]
    assert problem.utilities == [
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0]
    ]


def test_parsing():
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
    parser: PBParser = PBParser(multi_file_path)
    problem: PBMultiProblem = parser.multi_problem()
    verify_multi_example(problem)


def test_multi_writing():
    parser: PBParser = PBParser(multi_file_path)
    problem: PBMultiProblem = parser.multi_problem()

    writer: PBWriter = PBWriter(multi_test_file_path)
    writer.write(problem)

    # Parse Again
    parser = PBParser(multi_test_file_path)
    problem = parser.multi_problem()

    # Verify
    verify_multi_example(problem)

    os.remove(multi_test_file_path)
