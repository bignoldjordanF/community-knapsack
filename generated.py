from community_knapsack import *


def single_example():
    # Randomly generate a one-dimensional example
    # with between 10-20 projects and 10-100 voters.
    # The budget must be between 500-2000 and each
    # cost between 100-500. Approval voting is
    # used by voters:
    generator: PBGenerator = PBGenerator(
        num_projects=(10, 20),
        num_voters=(10, 100),
        budget_bound=(500, 2000),
        cost_bound=(100, 500),
        utility_bound=(0, 1)
    )
    problem: PBProblem = generator.generate()

    # Solve with e.g. ilp solver, greedy,
    # dynamic programming and fptas:
    ilp: PBResult = problem.solve(PBAlgorithm.ILP_SOLVER)
    greedy: PBResult = problem.solve(PBAlgorithm.GREEDY)
    dynprog: PBResult = problem.solve(PBAlgorithm.DYNAMIC_PROGRAMMING)
    fptas: PBResult = problem.solve(PBAlgorithm.FPTAS)

    print(ilp)
    print(greedy)
    print(dynprog)
    print(fptas)
    print()


def multi_example():
    # Randomly generate a two-dimensional example
    # with between 10-20 projects and 10-100 voters.
    # Both budgets must be between 500-2000 and each
    # cost between 100-500 for the first budget and
    # 50-400 for the second budget. Approval voting
    # is used by voters:
    generator: PBMultiGenerator = PBMultiGenerator(
        num_projects=(10, 20),
        num_voters=(10, 100),
        budget_bound=((500, 2000), (500, 2000)),
        cost_bound=((100, 500), (50, 400)),
        utility_bound=(0, 1)
    )
    problem: PBMultiProblem = generator.generate()

    # Solve with e.g. ilp solver, greedy,
    # memoization and genetic algorithm:
    ilp: PBResult = problem.solve(PBMultiAlgorithm.ILP_SOLVER)
    greedy: PBResult = problem.solve(PBMultiAlgorithm.GREEDY)
    memoization: PBResult = problem.solve(PBMultiAlgorithm.MEMOIZATION)
    genetic: PBResult = problem.solve(PBMultiAlgorithm.GENETIC_ALGORITHM)

    print(ilp)
    print(greedy)
    print(memoization)
    print(genetic)
    print()


if __name__ == '__main__':
    single_example()
    multi_example()
