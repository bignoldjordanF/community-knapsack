from community_knapsack import *
import ast
import os


# Get y-Axis
def get_y(results, num_problems, algorithm, tuple_idx):
    return [results[problem_idx][algorithm.name][tuple_idx] for problem_idx in range(num_problems)]


# Get y-Axes
def get_all_y(results, num_problems, algorithms, tuple_idx):
    return [get_y(results, num_problems, algorithm, tuple_idx) for algorithm in algorithms]


# Solve Problems
def solve_problems(problem_list, algorithms, timeout=120, max_fail=1, file_name=None, output=True):
    if file_name and os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return ast.literal_eval(''.join(file.readlines()))

    results = [{algorithm.name: (None, None, None) for algorithm in algorithms} for _ in range(len(problem_list))]
    for algorithm in algorithms:
        if output:
            print(f'Processing {algorithm.name}')

        fail_count = 0
        for pid, problem in enumerate(problem_list):
            if output:
                print(pid)

            result = problem.solve(algorithm, timeout=timeout)
            if result.runtime == timeout:
                fail_count += 1
            else:
                results[pid][algorithm.name] = (result.value, result.cost, result.runtime)
                fail_count = 0

            if fail_count == max_fail:
                break

    if file_name:
        with open(file_name, 'w+', encoding='utf-8') as file:
            file.writelines(str(results))

    return results
