from community_knapsack import PBMultiProblem, PBMultiAlgorithm, PBWriter, PBParser


if __name__ == '__main__':
    problem: PBMultiProblem = PBMultiProblem(
        num_projects=5,
        num_voters=5,
        budget=[1000, 250, 300],
        costs=[
            [200, 650, 400, 700, 400],
            [40, 100, 25, 65, 95],
            [60, 90, 120, 150, 130]
        ],
        utilities=[
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 5, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1],
        ]
    )
    x = problem.solve(PBMultiAlgorithm.MEMOIZATION)
    print(x)

    file_path: str = 'resources/generated/example.pb'
    PBWriter(file_path).write(problem)

    problem2: PBMultiProblem = PBParser(file_path).multi_problem()
    y = problem.solve(PBMultiAlgorithm.MEMOIZATION)
    print(y)

