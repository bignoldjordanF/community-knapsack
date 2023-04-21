from community_knapsack import PBParser, PBSingleProblem, PBSingleAlgorithm


if __name__ == '__main__':
    parser: PBParser = PBParser('../resources/pabulib/poland_warszawa_2017_aleksandrow.pb')
    problem: PBSingleProblem = parser.single_problem()
    print(problem.solve(PBSingleAlgorithm.BRANCH_AND_BOUND))
    print(problem.solve(PBSingleAlgorithm.ILP_SOLVER))
    print(problem.solve(PBSingleAlgorithm.GREEDY))
