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
    """
    Uses Borda count to convert ordinal preferences to utility values, i.e., give the
    least preferred item one point (vote), the next preferred two points, ..., and the
    most preferred n points.

    :param lookup: A lookup dictionary to find the index of an arbitrary project id in a project list.
    :param preferences: The preferences of a voter as a list of project ids from most to least preferred.
    :return: The utilities derived by a voter over all the projects.
    """
    # Begin with an empty list of zeroes for each project:
    utilities: List[int] = [0] * len(lookup)

    # The least preferred project gets one vote, and each
    # project after that gets one more than before:
    count: int = 1
    for preference in reversed(preferences):
        utilities[lookup[preference]] = count
        count += 1

    return utilities


def votes_to_utility(vote_type: str, lookup: Dict[int, int], votes: List[int], points: List[int]):
    """
    Converts votes over projects using some voting method (approval, cumulative, scoring or ordinal)
    into a utility list of all the projects. The returned list is a list of all the projects,
    where those that the voter has given preference or votes to have values, and the others
    have zero utility, e.g., voter_a approves 3,4,6: [0, 0, 0, 1, 1, 0, 1, 0].

    :param vote_type: The voting method or type used by the voter (approval, cumulative, scoring, ordinal).
    :param lookup: A lookup dictionary to find the index of an arbitrary project id in a project list.
    :param votes: The project ids that the voter is giving preferences over or votes to.
    :param points: Any points that the voter is giving to projects in cumulative or scoring voting.
    :return: A list of utilities that a voter gets over a list of projects.
    """
    # Begin with an empty list of zeroes for each project:
    utilities: List[int] = [0] * len(lookup)

    # Approval voting just gives a utility of one for all
    # projects the voter lists:
    if vote_type == 'approval':
        for vote in votes:
            utilities[lookup[vote]] = 1
        return utilities

    # Cumulative and scoring gives points utility for all
    # projects the voter lists:
    if vote_type in ('cumulative', 'scoring') and len(points) == len(votes):
        for pid, vote in enumerate(votes):
            utilities[lookup[vote]] = points[pid]

    # Ordinal voting uses the Borda count to obtain
    # utilities for each listed project:
    if vote_type == 'ordinal':
        return ordinal_to_utility(lookup, votes)

    # Any projects that were not included in the `votes`
    # list remain at zero utility:
    return utilities
