from typing import List, Dict


def aggregate_utilitarian(num_projects: int, utilities: List[List[int]]) -> List[int]:
    """
    Aggregates the multi-agent utilities by summing the votes for each project into a one-dimensional list.

    :param num_projects: The number of projects in the instance.
    :param utilities: A list of lists of utilities for each voter over the projects, i.e., utilities[v][p] is the
    utility voter v derives from project p.
    :return: A one-dimensional list of values for each project, i.e., values[i] is the value for project i.
    """

    return [
        sum(votes[idx] for votes in utilities)
        for idx in range(num_projects)
    ]


def resolve_project_ids(projects: List[int], allocation: List[int]) -> List[int]:
    """
    Resolves the project ids of the project indexes stored in allocation results.

    :param projects: A list of project ids typically passed into PBProblem instances.
    :param allocation: A list of project indexes representing an allocation or solution to the problem.
    :return: An allocation (list) of project ids rather than project indexes.
    """
    return [projects[idx] for _, idx in enumerate(allocation)]


def ordinal_to_utility(lookup: Dict[int, int], preferences: List[int]):
    elicited: int = len(lookup) - len(preferences)
    votes: int = elicited
    utilities: List[int] = [0] * len(lookup)
    for preference in reversed(preferences):
        utilities[lookup[preference]] = votes
        votes += 1
    return utilities


def votes_to_utility(vote_type: str, lookup: Dict[int, int], votes: List[int], points: List[int]):
    """

    :param vote_type:
    :param lookup:
    :param votes:
    :param points:
    :return:
    """
    utilities: List[int] = [0] * len(lookup)
    if vote_type == 'approval':
        for vote in votes:
            utilities[lookup[vote]] = 1
        return utilities

    if vote_type in ('cumulative', 'scoring') and len(points) == len(votes):
        for pid, vote in enumerate(votes):
            utilities[lookup[vote]] = points[pid]

    if vote_type == 'ordinal':
        return ordinal_to_utility(lookup, votes)

    return utilities
