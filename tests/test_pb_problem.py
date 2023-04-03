from community_knapsack.pbproblem import PBSingleProblem, \
    PBMultiProblem, \
    PBProblemError, \
    PBSingleAlgorithm, \
    PBMultiAlgorithm
from community_knapsack import PBParser
from typing import List, Tuple
import pytest


class TestPBProblem:
    """Ensures that instantiating PBProblem objects raise helpful errors and warnings when
    the input is incorrect."""

    def test_different_project_lengths(self):
        """Ensures a warning is shown if the `num_projects` parameter is incorrectly initialised."""
        with pytest.warns():
            PBSingleProblem(
                num_projects=5,
                num_voters=0,
                budget=10,
                costs=[5, 6],
                utilities=[],
                projects=[1, 2]
            )

    def test_different_voter_lengths(self):
        """Ensures a warning is shown if the `num_voter` parameter is incorrectly initialised."""
        with pytest.warns():
            PBSingleProblem(
                num_projects=2,
                num_voters=4,
                budget=10,
                costs=[5, 6],
                utilities=[[0, 1]],
                projects=[1, 2],
                voters=[1]
            )

    def test_different_utilities_length(self):
        """Ensures an error is thrown if there is an incorrect number of utilities."""
        with pytest.raises(PBProblemError):
            PBSingleProblem(
                num_projects=2,
                num_voters=2,
                budget=10,
                costs=[5, 6],
                utilities=[[0, 1]],
                projects=[1, 2],
                voters=[1, 2]
            )

    def test_bad_utilities_projects_length(self):
        """Ensures an error is thrown if there is an incorrect number of projects if any voter utility list."""
        with pytest.raises(PBProblemError):
            PBSingleProblem(
                num_projects=2,
                num_voters=2,
                budget=10,
                costs=[5, 6],
                utilities=[[0], [1, 0]],
                projects=[1, 2],
                voters=[1, 2]
            )


class TestPBSingleProblem:
    """Ensures that instantiating PBSingleProblem objects raise helpful errors and warnings when
    the input is incorrect."""

    def test_bad_costs(self):
        """Ensures an error is thrown if the number of costs is not equal to the number of projects."""
        with pytest.raises(PBProblemError):
            PBSingleProblem(
                num_projects=2,
                num_voters=2,
                budget=10,
                costs=[],
                utilities=[[0, 1], [1, 0]],
                projects=[1, 2],
                voters=[1, 2]
            )

    def test_success(self):
        """Ensures a valid PBSingleProblem can be created successfully, without errors or warnings."""
        PBSingleProblem(
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


class TestPBSingleSolving:
    """Ensures that solving PBSingleProblem objects returns allocations or produces warnings as
    expected."""

    single_problems: List[Tuple[PBSingleProblem, int]] = [
        (PBParser('resources/tests/pb/valid.pb').single_problem(), 7)
    ]
    exact_algorithms: List[PBSingleAlgorithm] = [
        PBSingleAlgorithm.BRUTE_FORCE,
        PBSingleAlgorithm.MEMOIZATION,
        PBSingleAlgorithm.DYNAMIC_PROGRAMMING,
        PBSingleAlgorithm.BRANCH_AND_BOUND
    ]
    approximation_algorithms: List[PBSingleAlgorithm] = [
        PBSingleAlgorithm.GREEDY,
        PBSingleAlgorithm.RATIO_GREEDY,
        PBSingleAlgorithm.FPTAS,
        PBSingleAlgorithm.SIMULATED_ANNEALING,
        PBSingleAlgorithm.GENETIC_ALGORITHM
    ]

    @pytest.mark.parametrize('problem,value', single_problems)
    @pytest.mark.parametrize('algorithm', exact_algorithms)
    def test_successful_allocations(self, problem: PBSingleProblem, value: int, algorithm: PBSingleAlgorithm):
        assert problem.solve(algorithm).value == value

    @pytest.mark.parametrize('problem,value', single_problems)
    @pytest.mark.parametrize('algorithm', approximation_algorithms)
    def test_successful_approximations(self, problem: PBSingleProblem, value: int, algorithm: PBSingleAlgorithm):
        assert abs(value - problem.solve(algorithm).value) <= 0.3 * value

    @pytest.mark.parametrize('problem,value', single_problems)
    @pytest.mark.parametrize('algorithm', exact_algorithms + approximation_algorithms)
    def test_timeout(self, problem: PBSingleProblem, value: int, algorithm: PBSingleAlgorithm):
        with pytest.warns():
            problem.solve(algorithm, timeout=0.1)


class TestPBMultiProblem:
    """Ensures that instantiating PBMultiProblem objects raise helpful errors and warnings when
    the input is incorrect."""

    def test_bad_budget_costs(self):
        """Ensures an error is thrown if the number of cost lists is not equal to the number of budgets."""
        with pytest.raises(PBProblemError):
            PBMultiProblem(
                num_projects=2,
                num_voters=2,
                budget=[10, 20],
                costs=[[3, 2]],
                utilities=[[0, 1], [1, 0]],
                projects=[1, 2],
                voters=[1, 2]
            )

    def test_bad_cost_lists(self):
        """Ensures an error is thrown if any of the cost lists does not have `num_projects` costs."""
        with pytest.raises(PBProblemError):
            PBMultiProblem(
                num_projects=2,
                num_voters=2,
                budget=[10, 20],
                costs=[[3, 2], [6]],
                utilities=[[0, 1], [1, 0]],
                projects=[1, 2],
                voters=[1, 2]
            )

    def test_success(self):
        """Ensures a valid PBMultiProblem can be created successfully, without errors or warnings."""
        PBMultiProblem(
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


class TestPBMultiSolving:
    """Ensures that solving PBMultiProblem objects returns allocations or produces warnings as
    expected."""

    multi_problems: List[Tuple[PBMultiProblem, int]] = [
        (PBParser('resources/tests/pb/multi_valid.pb').multi_problem(), 5)
    ]
    exact_algorithms: List[PBMultiAlgorithm] = [
        PBMultiAlgorithm.BRUTE_FORCE,
        PBMultiAlgorithm.MEMOIZATION
        # PBMultiAlgorithm.DYNAMIC_PROGRAMMING,
    ]
    approximation_algorithms: List[PBMultiAlgorithm] = [
        PBMultiAlgorithm.GREEDY,
        PBMultiAlgorithm.RATIO_GREEDY,
        PBMultiAlgorithm.BRANCH_AND_BOUND,
        PBMultiAlgorithm.SIMULATED_ANNEALING,
        PBMultiAlgorithm.GENETIC_ALGORITHM
    ]

    @pytest.mark.parametrize('problem,value', multi_problems)
    @pytest.mark.parametrize('algorithm', exact_algorithms)
    def test_successful_allocations(self, problem: PBMultiProblem, value: int, algorithm: PBMultiAlgorithm):
        assert problem.solve(algorithm).value == value

    @pytest.mark.parametrize('problem,value', multi_problems)
    @pytest.mark.parametrize('algorithm', approximation_algorithms)
    def test_successful_approximations(self, problem: PBMultiProblem, value: int, algorithm: PBMultiAlgorithm):
        assert abs(value - problem.solve(algorithm).value) <= 0.3 * value

    @pytest.mark.parametrize('problem,value', multi_problems)
    @pytest.mark.parametrize('algorithm', exact_algorithms + approximation_algorithms)
    def test_timeout(self, problem: PBMultiProblem, value: int, algorithm: PBMultiAlgorithm):
        with pytest.warns():
            problem.solve(algorithm, timeout=0.1)
