from community_knapsack import PBParser, PBSingleProblem, PBSingleAlgorithm


if __name__ == '__main__':
    parser: PBParser = PBParser('../resources/pabulib/small/poland_warszawa_2017_aleksandrow.pb')
    problem: PBSingleProblem = parser.single_problem()
    print(problem.solve(PBSingleAlgorithm.BRANCH_AND_BOUND, timeout=300))
    print(problem.solve(PBSingleAlgorithm.GREEDY))
