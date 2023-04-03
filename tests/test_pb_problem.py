from community_knapsack.pbproblem import PBSingleProblem, \
    PBMultiProblem, \
    PBProblemError
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
