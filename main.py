from community_knapsack import *

if __name__ == '__main__':

    import random
    # problem = PBProblem(
    #     num_projects=20,
    #     num_voters=15,
    #     budget=1_000_000,
    #     costs=[random.randint(50_000, 100_000) for _ in range(20)],
    #     utilities=[[random.randint(0, 10) for _ in range(25)] for _ in range(15)],
    # )
    #
    # greedy = problem.solve(PBAlgorithm.GREEDY)
    # ratio_greedy = problem.solve(PBAlgorithm.RATIO_GREEDY)
    # print(greedy)
    # print(ratio_greedy)
    # exact = problem.solve(PBAlgorithm.DYNAMIC_PROGRAMMING)
    # print(exact)
    # sim_anneal = problem.solve(PBAlgorithm.SIMULATED_ANNEALING)
    # print(sim_anneal)
    # genetic = problem.solve(PBAlgorithm.GENETIC_ALGORITHM)
    # print(genetic)

    problem = PBMultiProblem(
        num_projects=20,
        num_voters=15,
        budget=[1_000_000, 2_000_000, 300],
        costs=[
            [random.randint(50_000, 500_000) for _ in range(20)],
            [random.randint(50_000, 700_000) for _ in range(20)],
            [random.randint(20, 70) for _ in range(20)],
        ],
        utilities=[[random.randint(0, 10) for _ in range(20)] for _ in range(15)],
    )

    brute_force: PBResult = problem.solve(
        PBMultiAlgorithm.BRUTE_FORCE
    )
    print(brute_force)

    memoization: PBResult = problem.solve(
        PBMultiAlgorithm.MEMOIZATION
    )
    print(memoization)

    greedy: PBResult = problem.solve(
        PBMultiAlgorithm.GREEDY
    )
    print(greedy)

    ratio: PBResult = problem.solve(
        PBMultiAlgorithm.RATIO_GREEDY
    )
    print(ratio)

    branch_bound: PBResult = problem.solve(
        PBMultiAlgorithm.BRANCH_AND_BOUND
    )
    print(branch_bound)

    sim_anneal: PBResult = problem.solve(
        PBMultiAlgorithm.SIMULATED_ANNEALING
    )
    print(sim_anneal)

    genetic: PBResult = problem.solve(
        PBMultiAlgorithm.GENETIC_ALGORITHM
    )
    print(genetic)

