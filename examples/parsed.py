from community_knapsack import PBParser, PBSingleProblem, PBSingleAlgorithm


if __name__ == '__main__':
    parser: PBParser = PBParser('../resources/pabulib/poland_warszawa_2019_targowek-fabryczny-elsnerow-i-utrata.pb')
    problem: PBSingleProblem = parser.single_problem()
    print(problem.solve(PBSingleAlgorithm.DYNAMIC_PROGRAMMING))
