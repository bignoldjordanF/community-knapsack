from typing import Sequence, Tuple, Union, Optional, Dict, List, Callable
from community_knapsack import PBSingleProblem, \
    PBSingleAlgorithm, \
    PBMultiProblem, \
    PBMultiAlgorithm, \
    PBGenerator
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np
import json
import os


def generate_single_problems(
        num_project_bounds: Sequence[Tuple[int, int]],
        num_voters_bounds: Sequence[Tuple[int, int]],
        budget_bounds: Sequence[Tuple[int, int]],
        cost_bounds: Sequence[Tuple[int, int]],
        seed: int = 181
) -> List[PBSingleProblem]:
    """Generates the PBSingleProblem objects needed for an evaluation."""
    problems = []
    generator = PBGenerator(seed=seed)
    for num_projects_bound in num_project_bounds:
        for num_voters_bound in num_voters_bounds:
            for budget_bound in budget_bounds:
                for cost_bound in cost_bounds:
                    problems.append(generator.generate_single_problem(
                        num_projects_bound=num_projects_bound,
                        num_voters_bound=num_voters_bound,
                        budget_bound=budget_bound,
                        cost_bound=cost_bound
                    ))
    return problems


def generate_multi_problems(
        num_project_bounds: Sequence[Tuple[int, int]],
        num_voters_bounds: Sequence[Tuple[int, int]],
        dimension_bounds: Sequence[int],  # [1, 2]
        budget_bounds: Sequence[Sequence[Sequence[Tuple[int, int]]]],
        cost_bounds: Sequence[Sequence[Sequence[Tuple[int, int]]]],
        seed: int = 181
) -> List[PBMultiProblem]:
    """Generates the PBSingleProblem objects needed for an evaluation."""
    problems = []
    generator = PBGenerator(seed=seed)
    for num_projects_bound in num_project_bounds:
        for num_voters_bound in num_voters_bounds:
            for did, num_dimensions in enumerate(dimension_bounds):
                for budget_bound in budget_bounds[did]:
                    for cost_bound in cost_bounds[did]:
                        problems.append(generator.generate_multi_problem(
                            num_projects_bound=num_projects_bound,
                            num_voters_bound=num_voters_bound,
                            budget_bound=budget_bound,
                            cost_bound=cost_bound
                        ))

    return problems


def _solve_problems(
        solve_process: Callable,
        file_name: Optional[str] = None,
) -> Sequence[Dict[str, Tuple[float, float, float]]]:

    if file_name and not file_name.endswith('.json'):
        file_name += '.json'

    if file_name and os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)

    results = solve_process()

    if file_name:
        json_object = json.dumps(results)
        with open(file_name, 'w+', encoding='utf-8') as file:
            file.write(json_object)

    return results


def raw_solve_problems(
        problem_list: Sequence[Union[PBSingleProblem, PBMultiProblem]],
        algorithms: Sequence[Union[PBSingleAlgorithm, PBMultiAlgorithm]],
        file_name: Optional[str] = None,
        output: bool = False
) -> Sequence[Dict[str, Tuple[float, float, float]]]:
    """Solves a list of problems using the provided raw algorithms."""

    def raw_solve():
        results = [
                {algorithm.name: (None, None, None) for algorithm in algorithms}
                for _ in range(len(problem_list))
            ]

        for algorithm in algorithms:
            if output:
                print(f'Processing {algorithm.name}:')

            for pid, problem in enumerate(problem_list):
                if output:
                    print(pid)

                start = timer()
                result = algorithm(problem.budget, problem.costs, problem.values)
                end = timer()
                results[pid][algorithm.name] = (result[1], -1, (end - start) * 1000)

        return results

    return _solve_problems(raw_solve, file_name)


def solve_problems(
        problem_list: Sequence[Union[PBSingleProblem, PBMultiProblem]],
        algorithms: Sequence[Union[PBSingleAlgorithm, PBMultiAlgorithm]],
        timeout: int = -1,
        max_fail: int = -1,
        file_name: Optional[str] = None,
        output: bool = False
) -> Sequence[Dict[str, Tuple[float, float, float]]]:
    """Solves a list of problems using the provided algorithms."""

    def solve():
        results = [
            {algorithm.name: (None, None, None) for algorithm in algorithms}
            for _ in range(len(problem_list))
        ]

        for algorithm in algorithms:
            if output:
                print(f'Processing {algorithm.name}:')

            fail_count = 0
            for pid, problem in enumerate(problem_list):
                if output:
                    print(pid)

                result = problem.solve(algorithm, timeout=timeout)
                if result.runtime == timeout:
                    fail_count += 1
                else:
                    results[pid][algorithm.name] = \
                        (result.value, result.cost, result.runtime)
                    fail_count = 0

                if fail_count == max_fail:
                    break

        return results

    return _solve_problems(solve, file_name)


def get_y_axis(
        results: Sequence[Dict[str, Tuple[float, float, float]]],
        algorithm: Union[PBSingleAlgorithm, PBMultiAlgorithm],
        tuple_idx: int
) -> List[float]:
    """Returns a y-axis of values, costs or runtimes from a result set."""
    return [results[pid][algorithm.name][tuple_idx] for pid in range(len(results))]


def get_y_axes(
        results: Sequence[Dict[str, Tuple[float, float, float]]],
        algorithms: Sequence[Union[PBSingleAlgorithm, PBMultiAlgorithm]],
        tuple_idx: int
) -> List[List[float]]:
    """Returns a y-axes of values, costs or runtimes from a result set."""
    return [get_y_axis(results, algorithm, tuple_idx) for algorithm in algorithms]


def get_z_axis(
        results: Sequence[Sequence[Dict[str, Tuple[float, float, float]]]],
        algorithm: Union[PBSingleAlgorithm, PBMultiAlgorithm],
        tuple_idx: int
) -> List[List[float]]:
    """Returns a z-axis of values, costs or runtimes from a result set."""
    return [
        [y[algorithm.name][tuple_idx] if y[algorithm.name][tuple_idx] else np.nan for y in x]
        for x in results
    ]


def get_z_axes(
        results: Sequence[Sequence[Dict[str, Tuple[float, float, float]]]],
        algorithms: Sequence[Union[PBSingleAlgorithm, PBMultiAlgorithm]],
        tuple_idx: int
) -> List[List[List[float]]]:
    """Returns z-axes of values, costs or runtimes from a result set."""
    return [get_z_axis(results, algorithm, tuple_idx) for algorithm in algorithms]


ALGORITHM_PLOT_SET = {
    PBSingleAlgorithm.BRUTE_FORCE: ('BRF', 'grey'),
    PBMultiAlgorithm.BRUTE_FORCE: ('BRF', 'grey'),

    PBSingleAlgorithm.MEMOIZATION: ('MEM', '#ff7f0e'),
    PBMultiAlgorithm.MEMOIZATION: ('MEM', '#ff7f0e'),

    PBSingleAlgorithm.DYNAMIC_PROGRAMMING: ('DYP', '#1f77b4'),
    PBMultiAlgorithm.DYNAMIC_PROGRAMMING: ('DYP', '#1f77b4'),

    PBSingleAlgorithm.BRANCH_AND_BOUND: ('BRB', '#d62728'),
    PBMultiAlgorithm.BRANCH_AND_BOUND: ('ABR', '#2ca02c'),

    PBSingleAlgorithm.ILP_SOLVER: ('IPS', '#9467bd'),
    PBMultiAlgorithm.ILP_SOLVER: ('IPS', '#9467bd'),

    PBSingleAlgorithm.GREEDY: ('GRE', '#1f77b4'),
    PBMultiAlgorithm.GREEDY: ('GRE', '#1f77b4'),

    PBSingleAlgorithm.RATIO_GREEDY: ('RAG', '#ff7f0e'),
    PBMultiAlgorithm.RATIO_GREEDY: ('RAG', '#ff7f0e'),

    PBSingleAlgorithm.FPTAS: ('FPA', '#2ca02c'),

    PBSingleAlgorithm.SIMULATED_ANNEALING: ('SIA', '#d62728'),
    PBMultiAlgorithm.SIMULATED_ANNEALING: ('SIA', '#d62728'),

    PBSingleAlgorithm.GENETIC_ALGORITHM: ('GEN', '#9467bd'),
    PBMultiAlgorithm.GENETIC_ALGORITHM: ('GEN', '#9467bd'),
}
"""The plot legend label for each algorithm."""


# The default 2d plot settings if unspecified:
DEFAULT_LABEL = 'NULL'
DEFAULT_MARKER = 'o-'
DEFAULT_MARKER_SIZE = 4
DEFAULT_COLOR = 'grey'
DEFAULT_ALPHA = 1.0


def get_labels(algorithms: List[Union[PBSingleAlgorithm, PBMultiAlgorithm]]) -> List[str]:
    """Returns a list of labels for the algorithms passed to the function."""
    return [ALGORITHM_PLOT_SET[algorithm][0] for algorithm in algorithms]


def get_colors(algorithms: List[Union[PBSingleAlgorithm, PBMultiAlgorithm]]) -> List[str]:
    """Returns a list of colours for the algorithms passed to the function."""
    return [ALGORITHM_PLOT_SET[algorithm][1] for algorithm in algorithms]


def get_alphas(algorithms: List[Union[PBSingleAlgorithm, PBMultiAlgorithm]]) -> List[float]:
    """Returns a list of opacities for the algorithms passed to the function."""
    return [DEFAULT_ALPHA for _ in algorithms]


def get_sizes(algorithms: List[Union[PBSingleAlgorithm, PBMultiAlgorithm]]) -> List[int]:
    """Returns a list of sizes for the algorithms passed to the function."""
    return [DEFAULT_MARKER_SIZE for _ in algorithms]


def plot_2d(
        x_axis: Sequence[Union[int, float]],
        y_axes: Sequence[Sequence[Union[int, float]]],
        x_label: str = '',
        y_label: str = '',
        marker: Optional[str] = DEFAULT_MARKER,
        labels: Optional[Sequence[str]] = None,
        colors: Optional[Sequence[str]] = None,
        alphas: Optional[Sequence[float]] = None,
        sizes: Optional[Sequence[int]] = None,
        fix_x: Optional[Tuple[int, int]] = None,
        fix_y: Optional[Tuple[int, int]] = None,
        x_tick_limits: Optional[Tuple[int, int]] = None,
        x_ticks: Optional[Sequence[Union[int, float]]] = None,
        x_tick_minor: bool = False,
        filter_x: int = 0
) -> None:
    """Displays a plot showing the specified x and y data, and configured via
    the input parameters."""

    if filter_x > 0:
        x_axis = [x for xid, x in enumerate(x_axis) if xid % filter_x == 0]
        y_axes = [
            [y for yid, y in enumerate(y_axis) if yid % filter_x == 0]
            for y_axis in y_axes
        ]

    if not labels or len(labels) < len(y_axes):
        labels = [DEFAULT_LABEL] * len(y_axes)

    if not colors or len(colors) < len(y_axes):
        colors = [DEFAULT_COLOR] * len(y_axes)

    if not alphas or len(alphas) < len(y_axes):
        alphas = [DEFAULT_ALPHA] * len(y_axes)

    if not sizes or len(sizes) < len(y_axes):
        sizes = [DEFAULT_MARKER_SIZE] * len(y_axes)

    for yid, y_axis in enumerate(y_axes):
        plt.plot(
            x_axis,
            y_axis,
            marker,
            label=labels[yid],
            color=colors[yid],
            alpha=alphas[yid],
            markersize=sizes[yid]
        )

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.minorticks_on()
    plt.grid(which='both', alpha=0.2)

    ax = plt.gca()
    if x_tick_limits:
        ax.ticklabel_format(axis='x', style='sci', scilimits=x_tick_limits)
        ax.xaxis.offsetText.set_visible(False)

    if x_ticks:
        ax.set_xticks(x_ticks, minor=x_tick_minor)

    if fix_x:
        ax.set_xlim(fix_x)

    if fix_y:
        ax.set_ylim(fix_y)

    legend = plt.legend()
    for yid in range(len(y_axes)):
        legend.legend_handles[yid].set_markersize(DEFAULT_MARKER_SIZE)
        legend.legend_handles[yid].set_alpha(DEFAULT_ALPHA)

    plt.show()


def format_3d(
        flat_results: Sequence[Dict[str, Tuple[float, float, float]]],
        x_axis: Sequence[Union[int, float]],
        y_axis: Sequence[Union[int, float]]
) -> Sequence[Sequence[Dict[str, Tuple[float, float, float]]]]:
    """Formats a flat list of results into a 2d list for 3d plotting."""
    formatted_results = []
    current_result = 0

    for _ in x_axis:
        x_results = []
        for _ in y_axis:
            x_results.append(flat_results[current_result])
            current_result += 1
        formatted_results.append(x_results)

    return formatted_results


# The default 3d plot settings if unspecified:
DEFAULT_3D_MARKER_SIZE = 15


def get_3d_sizes(algorithms: List[Union[PBSingleAlgorithm, PBMultiAlgorithm]]) -> List[int]:
    """Returns a list of sizes for the algorithms passed to the function."""
    return [DEFAULT_3D_MARKER_SIZE for _ in algorithms]


def plot_3d(
        x_axis: Sequence[Union[int, float]],
        y_axis: Sequence[Union[int, float]],
        z_axes: Sequence[Sequence[Sequence[Union[int, float]]]],
        x_label: str = '',
        y_label: str = '',
        z_label: str = '',
        labels: Optional[Sequence[str]] = None,
        colors: Optional[Sequence[str]] = None,
        alphas: Optional[Sequence[float]] = None,
        sizes: Optional[Sequence[int]] = None,
        x_tick_limits: Optional[Tuple[int, int]] = None,
        y_tick_limits: Optional[Tuple[int, int]] = None,
        mpl_use: str = 'macosx'
):
    """Displays a plot showing the specified x, y and z data, and configured via
    the input parameters."""
    if len(mpl_use) >= 1:
        import matplotlib as mpl
        mpl.use(mpl_use)

    if not labels or len(labels) < len(z_axes):
        labels = [DEFAULT_LABEL] * len(z_axes)

    if not colors or len(colors) < len(z_axes):
        colors = [DEFAULT_COLOR] * len(z_axes)

    if not sizes or len(sizes) < len(z_axes):
        sizes = [DEFAULT_3D_MARKER_SIZE] * len(z_axes)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)

    all_x = [[x for _ in y_axis] for x in x_axis]
    all_y = [[y for y in y_axis] for _ in x_axis]

    for zid, z_axis in enumerate(z_axes):
        scatter = ax.scatter(
            all_x,
            all_y,
            [zt for zt in z_axis],
            label=labels[zid],
            c=colors[zid],
            s=sizes[zid]
        )
        if alphas and zid < len(alphas):
            scatter.set_alpha(alphas[zid])

    if x_tick_limits:
        ax.ticklabel_format(axis='x', style='sci', scilimits=x_tick_limits)
        ax.xaxis.offsetText.set_visible(False)

    if y_tick_limits:
        ax.ticklabel_format(axis='y', style='sci', scilimits=y_tick_limits)
        ax.yaxis.offsetText.set_visible(False)

    legend = plt.legend()
    for idx in range(len(z_axes)):
        legend.legend_handles[idx].set_sizes([DEFAULT_3D_MARKER_SIZE] * len(z_axes))
        legend.legend_handles[idx].set_alpha(DEFAULT_ALPHA)

    plt.show()
