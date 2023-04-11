from community_knapsack import *
num_projects = 50
num_voters = 3000
budget = 600_000

min_cost = 5_000
max_cost = 25_000
step_cost = 1_000

big_cost = 50_000

if __name__ == '__main__':
    generator = PBGenerator(
        seed=181
    )

    g = generator.generate_single_problem(
        num_projects_bound=(100, 100),
        num_voters_bound=(2000, 2000),
        budget_bound=(5000000, 5000000),
        cost_bound=(100000, 300000)
    )

    print(g.solve(PBSingleAlgorithm.ILP_SOLVER))
    print(g.solve(PBSingleAlgorithm.MEMOIZATION))

    # x = generator.generate_multi_problem(
    #     num_projects_bound=(50, 50),
    #     num_voters_bound=(2000, 2000),
    #     budget_bound=((100_000, 100_000), (50_000, 100_000), (100, 100)),
    #     cost_bound=((3_000, 8_000), (30, 50), (2, 5))
    # )
    # print(x.solve(PBMultiAlgorithm.MEMOIZATION))
    # print(x.solve(PBMultiAlgorithm.ILP_SOLVER))
