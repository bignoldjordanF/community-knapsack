from typing import List, Sequence


def aggregate_utilitarian(num_projects: int, utilities: Sequence[Sequence[int]]) -> List[int]:
    """
    Aggregates the multi-agent utilities over projects by summing the votes for each project into
    a one-dimensional list of values.

    :param num_projects: The number of projects in the instance (and thus `utilities`).
    :param utilities: A list of lists of utilities for each voter over the projects.
    :return: A one-dimensional list of values for each project, i.e., values[i] is the value for project i.
    """
    values: List[int] = [0] * num_projects

    for vid, utility in enumerate(utilities):
        if len(utility) != num_projects:
            raise ValueError(f'Voter {vid} has utilities for {len(utility)} projects but expected utilities '
                             f'for {num_projects} projects.')
        for pid, u in enumerate(utility):
            values[pid] += u

    return values


def ordinal_to_utility(
        num_projects: int,
        votes: Sequence[int],
        min_vote_length: int = -1,
        max_vote_length: int = -1
) -> List[int]:
    """
    Converts a list of ordinal preferences `votes` ordered from most to least preferred into a utility
    vector or list over the projects. This function should be called on a voter-by-voter basis, where
    votes contains the project *indexes* of the projects the voter 'prefers'. The min- and max-vote-
    length parameters are optional, but if they are equal then the Borda count algorithm is used, or
    otherwise the utilities are dictated by the number of preferences (projects) submitted.

    :param num_projects: The number of projects that votes was picked from, such that len(votes) <= num_projects.
    :param votes: A list of project *indexes* (not ids) that the voter `prefers`, s.t. len(votes) <= num_projects.
    :param min_vote_length: (Optional) The minimum number of preferences (projects) that the voter can submit.
    :param max_vote_length: (Optional) The maximum number of preferences (projects) that the voter can submit.
    :return: A `num_projects`-length list of utilities over all the projects, i.e., zero for all those not in votes.
    """
    # The votes list must only contain project ids:
    if num_projects < len(votes) or any(vote >= num_projects for vote in votes):
        raise ValueError('The vote list must only contain project indexes (not ids), and so there should '
                         'be no more than `num_projects` votes, and each project id should be < `num_projects`.')

    # The votes list must not contain duplicate projects:
    if len(set(votes)) != len(votes):
        raise ValueError('A single project was voted for more than once by a voter.')

    if 0 <= min_vote_length > len(votes):
        raise ValueError('There must be at least `min_vote_length` projects submitted when enabling minimum '
                         'vote length.')

    if 0 <= max_vote_length < len(votes):
        raise ValueError('There can at most `max_vote_length` projects submitted when enabling maximum vote length.')

    # Update Minimum & Maximum Vote Length
    if min_vote_length == -1:
        min_vote_length = 0

    if max_vote_length == -1:
        max_vote_length = num_projects

    utility: List[int] = [0] * num_projects

    # Use the Borda count if there is a limit on minimum and maximum vote length:
    if min_vote_length >= 0 and min_vote_length == max_vote_length:
        count: int = 1
        for preference in reversed(votes):
            utility[preference] = count
            count += 1
        return utility

    # TODO: Verify or prove this function
    # Otherwise, simulate cumulative voting by finding some score to distribute
    # over the projects based on the preferences not submitted:
    max_utility: int = min(num_projects, max_vote_length)
    not_submitted: int = max_utility - len(votes)
    current_utility: int = sum(k for k in range(1, not_submitted+1)) + 1

    for preference in reversed(votes):
        utility[preference] = current_utility
        current_utility += 1

    return utility


def vote_to_utility(
        num_projects: int,
        vote_type: str,
        votes: Sequence[int],
        points: Sequence[int] = None
) -> List[int]:
    """
    Converts a list of votes (and points in cumulative and scoring voting) into a utility vector or list
    over the projects. This function should be called on a voter-by-voter basis, where votes contains
    the project *indexes* of the projects the voter 'likes', and points is the corresponding number of
    votes/points/utility the voter gives to each project. That is, if votes[i]=3, then points[3] is
    the number of points the voter gives to project 3.

    Approval: The `votes` list contains the projects the voter approves.
    Cumulative: The voter has `x` votes to give to each project, denoted by the `votes` and `points` lists.
    Scoring: The voter scores each project, denoted by the `votes` and `points` lists.
    Ordinal: The voter submits preferences, where `votes` is in order from most to least preferred.

    :param num_projects: The number of projects that votes was picked from, such that len(votes) <= num_projects.
    :param vote_type: The type of voting method used, i.e., 'approval', 'cumulative', 'scoring' or 'ordinal'.
    :param votes: A list of project *indexes* (not ids) that the voter has `selected`, s.t. len(votes) <= num_projects.
    :param points: A list of corresponding points to each project id in vote (only in cumulative and scoring voting).
    :return: A `num_projects`-length list of utilities over all the projects, i.e., zero for all those not in votes.
    """
    # The vote type must be one of approval, cumulative, scoring or ordinal:
    if vote_type not in ('approval', 'cumulative', 'scoring', 'ordinal'):
        raise ValueError('The vote type must be one of "approval", "cumulative", "scoring" or "ordinal".')

    # The votes list must only contain project ids:
    if num_projects < len(votes) or any(vote >= num_projects for vote in votes):
        raise ValueError('The vote list must only contain project indexes (not ids), and so there should '
                         'be no more than `num_projects` votes, and each project id should be < `num_projects`.')

    # The votes list must not contain duplicate projects:
    if len(set(votes)) != len(votes):
        raise ValueError('A single project was voted for more than once by a voter.')

    if vote_type in ('cumulative', 'scoring'):
        # The points list must be the same length as votes for cumulative and scoring voting:
        if points is None or len(points) != len(votes):
            if points is None:
                points = []
            raise ValueError(f'There must be as many points ({len(points)} found) as votes ({len(votes)} found) in '
                             f'cumulative or scoring voting.')

    utility: List[int] = [0] * num_projects

    # Approval voting gives all projects in `votes` a utility of one:
    if vote_type == 'approval':
        for vote in votes:
            utility[vote] = 1
        return utility

    # Cumulative and scoring gives projects in `votes` their points:
    if vote_type in ('cumulative', 'scoring'):
        for idx, vote in enumerate(votes):
            utility[vote] = points[idx]
        return utility

    # Ordinal voting uses a different strategy:
    if vote_type in 'ordinal':
        return ordinal_to_utility(num_projects, votes)

    return utility
