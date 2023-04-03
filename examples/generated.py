from community_knapsack import PBGenerator, PBSingleProblem, PBSingleAlgorithm, PBResult


def main():
    generator: PBGenerator = PBGenerator()
    problem: PBSingleProblem = generator.generate_single_problem(
        num_projects_bound=(10, 20),
        num_voters_bound=(10, 100),
        budget_bound=(1000, 2000),
        cost_bound=(100, 750),
        utility_bound=(0, 5)
    )
    result: PBResult = problem.solve(PBSingleAlgorithm.RATIO_GREEDY)
    print(result)


if __name__ == '__main__':
    main()
