from community_knapsack import PBProblem, PBAlgorithm, PBWriter, PBParser


if __name__ == '__main__':
    problem: PBProblem = PBProblem(
        num_projects=5,
        num_voters=5,
        budget=1000,
        costs=[200, 650, 400, 700, 400],
        utilities=[
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 5, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1],
        ]
    )
    x = problem.solve(PBAlgorithm.DYNAMIC_PROGRAMMING)
    print(x)

    file_path: str = 'resources/generated/example.pb'
    PBWriter(file_path).write(problem)

    problem2: PBProblem = PBParser(file_path).problem()
    y = problem.solve(PBAlgorithm.DYNAMIC_PROGRAMMING)
    print(y)

