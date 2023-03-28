from community_knapsack import *

if __name__ == '__main__':
    # problem = PBProblem(
    #     num_projects=4,
    #     num_voters=5,
    #     budget=10_000,
    #     costs=[2_000, 6_000, 4_500, 5_000],
    #     utilities=[
    #         [1, 1, 0, 0],
    #         [0, 1, 0, 1],
    #         [0, 0, 0, 1],
    #         [0, 0, 1, 0],
    #         [0, 1, 1, 1]
    #     ],
    # )

    import random
    problem = PBProblem(
        num_projects=20,
        num_voters=10,
        budget=100,
        costs=[random.randint(10, 100) for _ in range(20)],
        utilities=[[random.randint(0, 1) for _ in range(20)] for _ in range(10)],
    )

    brute_force = problem.solve(
        PBAlgorithm.BRUTE_FORCE
    )

    memoization = problem.solve(
        PBAlgorithm.MEMOIZATION
    )

    dynamic_programming = problem.solve(
        PBAlgorithm.DYNAMIC_PROGRAMMING
    )

    branch_and_bound = problem.solve(
        PBAlgorithm.BRANCH_AND_BOUND
    )

    print(brute_force)
    print(memoization)
    print(dynamic_programming)
    print(branch_and_bound)

