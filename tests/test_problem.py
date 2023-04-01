import pytest
from community_knapsack import *


def test_project_warning():
    """A warning should be raised when `num_projects` != len(projects)."""
    with pytest.warns():
        PBProblem(
            num_projects=5,
            num_voters=2,
            budget=1000,
            costs=[20, 10, 20],
            utilities=[[1, 1, 0], [0, 1, 0]],
            projects=[3, 2, 1]  # != num_projects
        )


def test_voter_warning():
    """A warning should be raised when `num_voters` != len(voters)."""
    with pytest.warns():
        PBProblem(
            num_projects=3,
            num_voters=3,
            budget=1000,
            costs=[20, 10, 20],
            utilities=[[1, 1, 0], [0, 1, 0]],
            projects=[3, 2, 1],
            voters=[1, 2]  # != num_voters
        )


def test_missing_voter():
    """An error should be raised when `num_voters` != len(utilities)."""
    with pytest.raises(ValueError):
        PBProblem(
            num_projects=3,
            num_voters=3,
            budget=1000,
            costs=[20, 10, 20],
            utilities=[[1, 1, 0], [0, 1, 0]],  # missing voter
            projects=[3, 2, 1],
            voters=[1, 2, 3]
        )


def test_missing_utilities():
    """An error should be raised when `num_projects` != len(utilities[v])."""
    with pytest.raises(ValueError):
        PBProblem(
            num_projects=3,
            num_voters=3,
            budget=1000,
            costs=[20, 10, 20],
            utilities=[[1, 1, 0], [0, 1]],  # missing vote
            projects=[3, 2, 1],
            voters=[1, 2, 3]
        )


def test_missing_costs():
    """An error should be raised when `num_projects` != len(costs) in PBProblem."""
    with pytest.raises(ValueError):
        PBProblem(
            num_projects=3,
            num_voters=2,
            budget=1000,
            costs=[20, 20],
            utilities=[[1, 1, 0], [0, 1, 1]],
            projects=[3, 2, 1],
            voters=[1, 2]
        )


def test_missing_multi_costs():
    """An error should be raised when `len(budget)` != len(costs) in PBMultiProblem."""
    with pytest.raises(ValueError):
        PBMultiProblem(
            num_projects=3,
            num_voters=2,
            budget=[1000, 200],
            costs=[[200, 300, 600]],
            utilities=[[1, 1, 0], [0, 1, 1]],
            projects=[3, 2, 1],
            voters=[1, 2]
        )


def test_missing_multi_cost_values():
    """An error should be raised when `len(budget)` != len(costs) in PBMultiProblem."""
    with pytest.raises(ValueError):
        PBMultiProblem(
            num_projects=3,
            num_voters=2,
            budget=[1000, 200],
            costs=[[200, 300, 600], [75, 175]],
            utilities=[[1, 1, 0], [0, 1, 1]],
            projects=[3, 2, 1],
            voters=[1, 2]
        )
