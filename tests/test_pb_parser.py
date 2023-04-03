import community_knapsack.io.pbparser
from community_knapsack import PBParser,\
    PBSingleProblem, \
    PBMultiProblem, \
    PBSingleAlgorithm, \
    PBMultiAlgorithm
import pytest


class TestPBParsing:
    """Ensures the parsing process performs as expected and raises helpful errors and
    warnings when an error occurs with a .pb file."""

    def test_bad_file_path(self):
        """The parser should raise an error when a bad .pb file path is entered."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('bad_file_path.pb')

    def test_bad_syntax(self):
        """The parser should raise an error when a .pb (csv) file has bad syntax."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            p = PBParser('resources/tests/pb/bad_syntax.pb')
            r = p.multi_problem()
            print(r.costs)

    def test_bad_budget(self):
        """The parser should raise an error when a non-numeric budget is entered."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_budget.pb')

    def test_missing_budget(self):
        """The parser should raise an error when zero budgets are entered."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/missing_budget.pb')

    def test_bad_vote_type(self):
        """The parser should raise an error when a bad vote type is entered."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_vote_type.pb')

    def test_missing_cost(self):
        """The parser should raise an error when a project has no cost."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/missing_cost.pb')

    def test_bad_cost(self):
        """The parser should raise an error when a project has the wrong number of costs."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_cost.pb')

    def test_bad_selected(self):
        """The parser should raise a warning when a project has an invalid `selected` value."""
        with pytest.warns():
            PBParser('resources/tests/pb/bad_selected.pb')

    def test_duplicate_vote(self):
        """The parser should raise an error when a voter has voted for the same project more than once."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/duplicate_vote.pb')

    def test_bad_votes_points(self):
        """The parser should raise an error when a voter has a different number of votes to points in
        cumulative or scoring voting types."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_vote_points.pb')

    def test_bad_vote(self):
        """The parser should raise an error when a voter votes for a non-existent project."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_vote.pb')

    def test_bad_points(self):
        """The parser should raise an error when points given to a project are non-positive integers in
        cumulative or scoring voting types."""
        with pytest.raises(community_knapsack.io.pbparser.PBParserError):
            PBParser('resources/tests/pb/bad_points.pb')

    def test_success(self):
        """Ensures a valid .pb file can be parsed successfully, without errors or warnings."""
        problem: PBSingleProblem = PBParser('resources/tests/pb/valid.pb').single_problem()
        assert problem.num_projects == 5
        assert problem.num_voters == 5
        assert problem.budget == 100
        assert problem.costs == [50, 75, 90, 20, 10]
        assert problem.utilities == [
            [1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
        ]
        assert problem.projects == ['5', '6', '7', '8', '9']
        assert problem.voters == ['1', '2', '3', '4', '5']

    def test_single_as_multi_success(self):
        """Ensures a valid (single) .pb file can be parsed as a multi-problem successfully,
         without errors or warnings."""
        problem: PBMultiProblem = PBParser('resources/tests/pb/valid.pb').multi_problem()
        assert problem.num_projects == 5
        assert problem.num_voters == 5
        assert problem.budget == [100]
        assert problem.costs == [[50, 75, 90, 20, 10]]
        assert problem.utilities == [
            [1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
        ]
        assert problem.projects == ['5', '6', '7', '8', '9']
        assert problem.voters == ['1', '2', '3', '4', '5']

    def test_multi_success(self):
        """Ensures a valid (multi) .pb file can be parsed successfully, without errors or warnings."""
        problem: PBMultiProblem = PBParser('resources/tests/pb/multi_valid.pb').multi_problem()
        assert problem.num_projects == 5
        assert problem.num_voters == 5
        assert problem.budget == [100, 200]
        assert problem.costs == [[50, 75, 90, 20, 10], [75, 100, 90, 50, 85]]
        assert problem.utilities == [
            [1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
        ]
        assert problem.projects == ['5', '6', '7', '8', '9']
        assert problem.voters == ['1', '2', '3', '4', '5']

    def test_single_solve_success(self):
        """Ensures parsing a valid single .pb file results in the correct allocation value."""
        problem: PBSingleProblem = PBParser('resources/tests/pb/valid.pb').single_problem()
        assert problem.solve(PBSingleAlgorithm.BRUTE_FORCE).value == 7

    def test_multi_solve_success(self):
        """Ensures parsing a valid multi .pb file results in the correct allocation value."""
        problem: PBMultiProblem = PBParser('resources/tests/pb/multi_valid.pb').multi_problem()
        assert problem.solve(PBMultiAlgorithm.BRUTE_FORCE).value == 5
