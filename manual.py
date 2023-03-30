from community_knapsack import PBProblem, \
    PBAlgorithm, \
    PBMultiProblem,\
    PBMultiAlgorithm,\
    PBResult


def simple_example():
    # A very simple example problem with
    # five voters using approval voting
    # over five projects:
    problem: PBProblem = PBProblem(
        num_projects=5,
        num_voters=5,
        budget=1000,
        costs=[200, 650, 400, 700, 400],
        utilities=[
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1],
        ]
    )

    # Solve with e.g. greedy, ratio greedy,
    # branch and bound and genetic algorithm:
    greedy: PBResult = problem.solve(PBAlgorithm.GREEDY)
    ratio_greedy: PBResult = problem.solve(PBAlgorithm.RATIO_GREEDY)
    branch_bound: PBResult = problem.solve(PBAlgorithm.BRANCH_AND_BOUND)
    genetic: PBResult = problem.solve(PBAlgorithm.GENETIC_ALGORITHM)

    print(greedy)
    print(ratio_greedy)
    print(branch_bound)
    print(genetic)
    print()


def multi_example():
    # A simple example problem with three
    # constraints, and five voters using
    # approval voting over five projects:
    problem: PBMultiProblem = PBMultiProblem(
        num_projects=5,
        num_voters=5,
        budget=[1000, 200, 100],
        costs=[
            [200, 650, 400, 700, 400],
            [50, 75, 100, 75, 50],
            [50, 25, 5, 40, 50]
        ],
        utilities=[
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0],
        ]
    )

    # Solve with e.g. ratio greedy, approximate branch and bound
    # and simulated annealing:
    ratio_greedy: PBResult = problem.solve(PBMultiAlgorithm.RATIO_GREEDY)
    branch_and_bound: PBResult = problem.solve(PBMultiAlgorithm.BRANCH_AND_BOUND)
    simulated_annealing: PBResult = problem.solve(PBMultiAlgorithm.SIMULATED_ANNEALING)

    print(ratio_greedy)
    print(branch_and_bound)
    print(simulated_annealing)
    print()


if __name__ == '__main__':
    simple_example()
    multi_example()
