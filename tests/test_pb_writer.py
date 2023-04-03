import community_knapsack.io.pbparser
from community_knapsack import PBWriter,\
    PBParser, \
    PBSingleProblem, \
    PBMultiProblem, \
    PBSingleAlgorithm, \
    PBMultiAlgorithm, \
    PBResult
import os


class TestPBWriting:
    """Ensures the writing process performs as expected."""

    def test_successful_single_write(self):
        """Ensures writing a single problem and parsing it results in the same data."""
        problem: PBSingleProblem = PBSingleProblem(
            num_projects=5,
            num_voters=5,
            budget=100,
            costs=[20, 50, 75, 40, 45],
            utilities=[
                [1, 0, 1, 1, 1],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 1],
                [1, 1, 0, 1, 0],
                [0, 0, 0, 1, 1]
            ],
            projects=['30', '44', '20', '25', '22'],
            voters=[1, 2, 3, 4, 5]
        )
        file_path: str = 'resources/tests/generated/problem.pb'
        writer: PBWriter = PBWriter(file_path)
        writer.write(problem)

        parser: PBParser = PBParser(file_path)
        problem = parser.problem()

        assert problem.num_projects == 5
        assert problem.num_voters == 5
        assert problem.budget == 100
        assert problem.costs == [20, 50, 75, 40, 45]
        assert problem.utilities == [
            [1, 0, 1, 1, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 1, 1]
        ]
        assert problem.projects == ['30', '44', '20', '25', '22']
        assert problem.voters == ['1', '2', '3', '4', '5']

        os.remove(file_path)

    def test_successful_multi_write(self):
        """Ensures writing a multi problem and parsing it results in the same data."""
        problem: PBMultiProblem = PBMultiProblem(
            num_projects=5,
            num_voters=5,
            budget=[100, 200],
            costs=[[20, 50, 75, 40, 45], [50, 75, 100, 90, 80]],
            utilities=[
                [1, 0, 1, 1, 1],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 0, 1],
                [1, 1, 0, 1, 0],
                [0, 0, 0, 1, 1]
            ],
            projects=['30', '44', '20', '25', '22'],
            voters=[1, 2, 3, 4, 5]
        )
        file_path: str = 'resources/tests/generated/multi_problem.pb'
        writer: PBWriter = PBWriter(file_path)
        writer.write(problem)

        parser: PBParser = PBParser(file_path)
        problem = parser.multi_problem()

        assert problem.num_projects == 5
        assert problem.num_voters == 5
        assert problem.budget == [100, 200]
        assert problem.costs == [[20, 50, 75, 40, 45], [50, 75, 100, 90, 80]]
        assert problem.utilities == [
            [1, 0, 1, 1, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 1],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 1, 1]
        ]
        assert problem.projects == ['30', '44', '20', '25', '22']
        assert problem.voters == ['1', '2', '3', '4', '5']

        os.remove(file_path)
