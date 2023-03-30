from community_knapsack import *


if __name__ == '__main__':
    # Parse a locally stored .pb file from Pabulib.org:
    parser: PBParser = PBParser('resources/pabulib/poland_warszawa_2023_ochota.pb')
    problem: PBProblem = parser.problem()

    # Obtain the predefined allocation (if any):
    predefined: PBResult = parser.predefined_result()

    # Solve using e.g. greedy, genetic, simulated annealing:
    greedy: PBResult = problem.solve(PBAlgorithm.GREEDY)
    genetic: PBResult = problem.solve(PBAlgorithm.GENETIC_ALGORITHM)
    memoization: PBResult = problem.solve(PBAlgorithm.SIMULATED_ANNEALING)

    print(greedy)
    print(genetic)
    print(memoization)
