from community_knapsack import *

if __name__ == '__main__':

    import random
    problem = PBMultiProblem(
        num_projects=15,
        num_voters=15,
        budget=[50_000, 10_000, 25_000],
        costs=[
            [random.randint(5_000, 20_000) for _ in range(15)],
            [random.randint(1_000, 2_000) for _ in range(15)],
            [random.randint(1_000, 3_000) for _ in range(15)]
        ],
        utilities=[[random.randint(0, 10) for _ in range(15)] for _ in range(15)],
    )

    brute_force: PBResult = problem.solve(
        PBMultiAlgorithm.BRUTE_FORCE
    )
    print(brute_force)

    memoization: PBResult = problem.solve(
        PBMultiAlgorithm.MEMOIZATION
    )
    print(memoization)
