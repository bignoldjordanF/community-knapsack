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
        num_projects=30,
        num_voters=15,
        budget=500_000,
        costs=[random.randint(30_000, 100_000) for _ in range(30)],
        utilities=[[random.randint(0, 10) for _ in range(30)] for _ in range(15)],
    )

    # brute_force: PBResult = problem.solve(
    #     PBAlgorithm.BRUTE_FORCE
    # )
    # print(brute_force)

    memoization: PBResult = problem.solve(
        PBAlgorithm.MEMOIZATION
    )
    print(memoization)

    # dynamic_programming: PBResult = problem.solve(
    #     PBAlgorithm.DYNAMIC_PROGRAMMING
    # )
    # print(dynamic_programming)

    branch_and_bound: PBResult = problem.solve(
        PBAlgorithm.BRANCH_AND_BOUND
    )
    print(branch_and_bound)

    fptas: PBResult = problem.solve(
        PBAlgorithm.FPTAS
    )
    print(fptas)

    simulated_annealing: PBResult = problem.solve(
        PBAlgorithm.SIMULATED_ANNEALING
    )
    print(simulated_annealing)
