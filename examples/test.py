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

    g = generator.generate_multi_problem(
        num_projects_bound=(150, 150),
        num_voters_bound=(3000, 3000),
        budget_bound=((100_000, 100_000), (100, 100), (200, 200), (200, 200), (200, 200)),
        cost_bound=((5_000, 10_000), (1, 5), (1, 10), (1, 10), (50, 50))
    )
    print(g.solve(PBMultiAlgorithm.MEMOIZATION))
