from community_knapsack import PBMultiProblem, PBMultiAlgorithm, PBWriter, PBParser, PBMultiGenerator


if __name__ == '__main__':
    generator: PBMultiGenerator = PBMultiGenerator(
        num_projects=60,
        num_voters=1000,
        budget_bound=((500_000, 2_000_000), (200_000, 1_000_000)),
        cost_bound=((50_000, 100_000), (25_000, 75_000)),
        utility_bound=(0, 5)
    )
    problem: PBMultiProblem = generator.generate()
    x = problem.solve(PBMultiAlgorithm.ILP_SOLVER)
    print(x)

    file_path: str = 'resources/generated/example.pb'
    PBWriter(file_path).write(problem)
    problem2: PBMultiProblem = PBParser(file_path).multi_problem()

    y = problem2.solve(PBMultiAlgorithm.ILP_SOLVER)
    print(y)
