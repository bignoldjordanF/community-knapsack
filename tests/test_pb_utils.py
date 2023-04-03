from community_knapsack import pbutils
import pytest


class TestVoteAggregation:
    """Ensures the vote aggregation utility functions return the correct results and
    raise helpful errors and warnings when the input is incorrect."""

    def test_utilitarian_bad_utilities(self):
        with pytest.raises(ValueError):
            pbutils.aggregate_utilitarian(5, [[0, 1, 1, 0, 1], [0, 1]])

    def test_utilitarian_aggregation(self):
        assert pbutils.aggregate_utilitarian(5, [[0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [1, 0, 0, 0, 1]]) == \
               [1, 2, 2, 1, 2]


class TestVoteConversion:
    """Ensures the vote conversion utility functions return the correct results and raise
    helpful errors and warnings when the input is incorrect."""

    def test_bad_vote_type(self):
        """Ensures that the vote type must be one of approval, cumulative, scoring or ordinal."""
        with pytest.raises(ValueError):
            pbutils.vote_to_utility(num_projects=5, vote_type='what?', votes=[], points=[])

    def test_too_many_votes(self):
        """Ensures that there is at most `num_projects` votes in the votes list."""
        with pytest.raises(ValueError):
            pbutils.vote_to_utility(num_projects=5, vote_type='approval', votes=[1, 2, 3, 4, 5, 6], points=[])

    def test_bad_project_vote(self):
        """Ensures that there are only project indexes in the votes list."""
        with pytest.raises(ValueError):
            pbutils.vote_to_utility(num_projects=5, vote_type='approval', votes=[1, 2, 354, 4, 5, 6], points=[])

    def test_duplicate_vote(self):
        """Ensures that each project is voted for at most once by a voter."""
        with pytest.raises(ValueError):
            pbutils.vote_to_utility(num_projects=5, vote_type='approval', votes=[2, 2], points=[])

    def test_missing_points(self):
        """Ensures that there are only project indexes in the votes list."""
        with pytest.raises(ValueError):
            pbutils.vote_to_utility(num_projects=5, vote_type='cumulative', votes=[0, 1, 2, 3, 4])
            pbutils.vote_to_utility(num_projects=5, vote_type='scoring', votes=[0, 1, 2, 3, 4], points=[2])

    def test_ordinal_too_many_votes(self):
        """Ensures that there is at most `num_projects` votes in the votes list."""
        with pytest.raises(ValueError):
            pbutils.ordinal_to_utility(num_projects=5, votes=[1, 2, 3, 4, 5])

    def test_ordinal_bad_project_vote(self):
        """Ensures that there are only project indexes in the votes list."""
        with pytest.raises(ValueError):
            pbutils.ordinal_to_utility(num_projects=5, votes=[1, 2, 354, 4, 5, 6])

    def test_ordinal_min_vote_length(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        with pytest.raises(ValueError):
            pbutils.ordinal_to_utility(num_projects=5, votes=[], min_vote_length=1)

    def test_ordinal_max_vote_length(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        with pytest.raises(ValueError):
            pbutils.ordinal_to_utility(num_projects=5, votes=[1, 2], max_vote_length=1)

    def test_empty_success(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=0,
            vote_type='cumulative',
            votes=[],
            points=[]
        ) == []

    def test_approval_voting_success(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=5,
            vote_type='approval',
            votes=[0, 1, 4]
        ) == [1, 1, 0, 0, 1]

    def test_cumulative_voting_success(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=5,
            vote_type='cumulative',
            votes=[2, 4],
            points=[10, 11]
        ) == [0, 0, 10, 0, 11]

    def test_scoring_voting_success(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=5,
            vote_type='scoring',
            votes=[2, 3],
            points=[10, 11]
        ) == [0, 0, 10, 11, 0]

    def test_ordinal_voting_success(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=5,
            vote_type='ordinal',
            votes=[2, 3]
        ) == [0, 0, 8, 7, 0]

    def test_ordinal_voting_success_2(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.vote_to_utility(
            num_projects=5,
            vote_type='ordinal',
            votes=[2, 3, 1]
        ) == [0, 4, 6, 5, 0]

    def test_borda_count(self):
        """Ensures that there are at most min_vote_length preferences submitted."""
        assert pbutils.ordinal_to_utility(
            num_projects=5,
            votes=[2, 3, 1],
            min_vote_length=3,
            max_vote_length=3
        ) == [0, 1, 3, 2, 0]
