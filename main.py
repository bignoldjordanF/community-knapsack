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
        num_projects=15,
        num_voters=10,
        budget=100_000,
        costs=[random.randint(25_000, 100_000) for _ in range(15)],
        utilities=[[random.randint(0, 1) for _ in range(15)] for _ in range(10)],
    )

    brute_force = problem.solve(
        PBAlgorithm.BRUTE_FORCE
    )

    memoization = problem.solve(
        PBAlgorithm.MEMOIZATION
    )

    print(brute_force)
    print(memoization)

