from community_knapsack import PBResult, PBSingleProblem, PBSingleAlgorithm


if __name__ == '__main__':
    problem: PBSingleProblem = PBSingleProblem(
        num_projects=5,
        num_voters=5,
        budget=100,
        costs=[50, 25, 75, 45, 60],
        utilities=[
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 0, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 1]
        ]
    )
    result: PBResult = problem.solve(PBSingleAlgorithm.BRANCH_AND_BOUND)
    print(result)
