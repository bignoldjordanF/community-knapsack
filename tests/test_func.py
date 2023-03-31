from community_knapsack.pbfunc import *


def test_aggregate_utilitarian():
    # Essentially just summing the votes for each project:
    num_projects: int = 5
    utilities: List[List[int]] = [
        [2, 3, 0, 5, 4],
        [3, 0, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [4, 9, 5, 3, 2]
    ]
    assert aggregate_utilitarian(num_projects, utilities) == [10, 13, 7, 10, 7]


def test_resolve_project_ids():
    # Converting an allocation of project indexes to an
    # allocation of project ids:
    projects: List[int] = [4, 9, 10, 12, 13]
    allocation: List[int] = [0, 2, 3]
    assert resolve_project_ids(projects, allocation) == [4, 10, 12]


def test_ordinal_to_utility():
    # Converting a list of projects ids denoting most to least preferred
    # to a list of utility values using Borda count:
    lookup: Dict[int, int] = {4: 0, 9: 1, 10: 2, 12: 3, 13: 4}
    preferences: List[int] = [13, 9, 10]
    assert votes_to_utility('ordinal', lookup, preferences, []) == [0, 2, 1, 0, 3]


def test_approval_to_utility():
    lookup: Dict[int, int] = {4: 0, 9: 1, 10: 2, 12: 3, 13: 4}
    votes: List[int] = [9, 10, 12]
    assert votes_to_utility('approval', lookup, votes, []) == [0, 1, 1, 1, 0]


def test_cumulative_scoring_to_utility():
    lookup: Dict[int, int] = {4: 0, 9: 1, 10: 2, 12: 3, 13: 4}
    votes: List[int] = [10, 4, 13]
    points: List[int] = [4, 5, 2]
    assert votes_to_utility('cumulative', lookup, votes, points) == [5, 0, 4, 0, 2]
    assert votes_to_utility('scoring', lookup, votes, points) == [5, 0, 4, 0, 2]


