from community_knapsack import PBParser, PBSingleProblem, PBSingleAlgorithm, pbutils


if __name__ == '__main__':
    parser: PBParser = PBParser('../resources/pabulib/small/poland_warszawa_2017_aleksandrow.pb')
    problem: PBSingleProblem = parser.problem()
    print(pbutils.aggregate_utilitarian(problem.num_projects, problem.utilities))
    print(problem.solve(PBSingleAlgorithm.BRANCH_AND_BOUND))
    print(problem.solve(PBSingleAlgorithm.GREEDY))
