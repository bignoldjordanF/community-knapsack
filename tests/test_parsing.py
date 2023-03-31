from community_knapsack import *


def test_parsing():
    parser: PBParser = PBParser('resources/demonstration/example.pb')
    problem: PBProblem = parser.problem()
    assert problem.num_projects == 5
    assert problem.num_voters == 5
