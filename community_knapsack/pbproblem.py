from . import pbfunc
from . import solvers

from collections import namedtuple
from timeit import default_timer
from typing import List
from enum import Enum


PBResult = namedtuple('PBResult', ('allocation', 'value', 'runtime', 'algorithm', 'approximate'))
"""A named-tuple for allocation results, containing the allocation as
a list of project ids, its overall value and the runtime in milliseconds."""


class PBAlgorithm(Enum):
    BRUTE_FORCE = 0
    """A very slow but exact algorithm that enumerates every possible allocation and returns the best (optimal) one.
    This is likely too slow and is very rarely applicable."""

    MEMOIZATION = 1
    """A relatively slow pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster
    result."""

    DYNAMIC_PROGRAMMING = 2
    """A relatively slow pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster
    result."""

    BRANCH_AND_BOUND = 3
    """An exact algorithm that begins to enumerate every possible allocation but prunes certain branches
    for a faster result. The run-time is exponential (slow) but can be much faster depending on the problem."""

    FPTAS = 4
    """A relatively fast algorithm that uses the dynamic programming algorithm to find an approximation within
    50% of the optimal allocation. A very good option for larger problem sizes where exact algorithms are too slow."""

    SIMULATED_ANNEALING = 5
    """A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation."""

    GENETIC_ALGORITHM = 6
    """A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution."""

    GREEDY = 7
    """A fast approximation algorithm that picks projects by their overall value. This is commonly used
    in real-world budget allocations."""

    RATIO_GREEDY = 8
    """A fast and typically better (vs. greedy) approximation algorithm that picks projects by their overall
    value-to-weight ratio."""

    ILP_SOLVER = 9
    """A branch-and-cut integer programming solver using the PuLP library. This is typically fast, although
    it can be slow for larger instances."""

    def is_approximate(self) -> bool:
        """
        :return: True if the algorithm is an approximation scheme, or false for exact algorithms.
        """
        return self in (
            PBAlgorithm.GREEDY,
            PBAlgorithm.RATIO_GREEDY,
            PBAlgorithm.FPTAS,
            PBAlgorithm.SIMULATED_ANNEALING,
            PBAlgorithm.GENETIC_ALGORITHM
        )


class PBProblem:
    def __init__(
            self,
            num_projects: int,
            num_voters: int,
            budget: int,
            costs: List[int],
            utilities: List[List[int]],
            projects: List[int] = None,
            voters: List[int] = None,
    ):
        """
        Instantiates a single-dimensional (one constraint) participatory budgeting problem.

        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param budget: The single fixed budget of the instance.
        :param costs: A list of costs for each project, i.e., costs[i] is the cost of project i.
        :param utilities: A list of lists of utilities for each voter over the projects, i.e., utilities[v][p] is the
        utility voter v derives from project p.
        :param projects: An optional list of custom project ids, defaulting to 0,...,num_projects-1 otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 0,...,num_voters-1 otherwise.
        """
        self.num_projects: int = num_projects
        self.num_voters: int = num_voters
        self.budget: int = budget
        self.costs: List[int] = costs
        self.utilities: List[List[int]] = utilities
        self.projects: List[int] = projects if projects else [idx for idx in range(num_projects)]
        self.voters: List[int] = voters if voters else [idx for idx in range(num_voters)]

    def __str__(self) -> str:
        """
        :return: A string representing the problem data.
        """
        return str(self.__dict__)

    def solve(self, algorithm: PBAlgorithm) -> PBResult:
        """
        Reduces a one-dimensional participatory budgeting problem to the one-dimensional knapsack problem
        and solves it using the specified algorithm.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :return: The optimal allocation for the problem, its overall value and the run-time in milliseconds.
        """
        start_time: float = default_timer()

        values: List[int] = pbfunc.aggregate_utilitarian(
            self.num_projects,
            self.utilities,
        )

        allocation = PBResult([], 0, 0.0, algorithm, None)

        if algorithm == PBAlgorithm.BRUTE_FORCE:
            allocation = solvers.brute_force(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.MEMOIZATION:
            allocation = solvers.memoization(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.DYNAMIC_PROGRAMMING:
            allocation = solvers.dynamic_programming(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.BRANCH_AND_BOUND:
            allocation = solvers.branch_and_bound(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.FPTAS:
            allocation = solvers.fptas(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.SIMULATED_ANNEALING:
            allocation = solvers.simulated_annealing(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.GENETIC_ALGORITHM:
            allocation = solvers.genetic_algorithm(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.GREEDY:
            allocation = solvers.greedy(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.RATIO_GREEDY:
            allocation = solvers.ratio_greedy(self.budget, self.costs, values)

        elif algorithm == PBAlgorithm.ILP_SOLVER:
            allocation = solvers.integer_programming(self.budget, self.costs, values)

        end_time: float = default_timer()

        return PBResult(
            allocation=pbfunc.resolve_project_ids(
                self.projects,
                allocation[0]
            ),
            value=allocation[1],
            runtime=(end_time - start_time) * 1000,
            algorithm=str(algorithm),
            approximate=algorithm.is_approximate()
        )

    def approximate(self) -> PBResult:
        ratio_greedy: PBResult = self.solve(PBAlgorithm.RATIO_GREEDY)
        fptas: PBResult = self.solve(PBAlgorithm.FPTAS)
        simulated_annealing: PBResult = self.solve(PBAlgorithm.SIMULATED_ANNEALING)
        genetic_algorithm: PBResult = self.solve(PBAlgorithm.GENETIC_ALGORITHM)
        return max([ratio_greedy, fptas, simulated_annealing, genetic_algorithm], key=lambda r: r.value)


class PBMultiAlgorithm(Enum):
    BRUTE_FORCE = 0
    """A very slow but exact algorithm that enumerates every possible allocation and returns the best (optimal) one.
    This is likely too slow and is very rarely applicable."""

    MEMOIZATION = 1
    """A relatively slow exact algorithm that improves upon the brute force algorithm for a faster result."""

    DYNAMIC_PROGRAMMING = 2
    """An exact algorithm that improves upon the brute force algorithm, but is still extremely slow given larger
    problem sizes, especially with multiple dimensions. This is very rarely applicable."""

    BRANCH_AND_BOUND = 3
    """An approximation algorithm that begins to enumerate every possible allocation but prunes 
    certain branches for a faster result. The run-time is exponential (slow) but can be much 
    faster depending on the problem."""

    SIMULATED_ANNEALING = 4
    """A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation."""

    GENETIC_ALGORITHM = 5
    """A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution."""

    GREEDY = 7
    """A fast approximation algorithm that picks projects by their overall value. This is commonly used
    in real-world budget allocations."""

    RATIO_GREEDY = 8
    """A fast and typically better (vs. greedy) approximation algorithm that picks projects by their overall
    value-to-weight ratio, where weight is the sum of all weights for each item."""

    ILP_SOLVER = 9
    """A branch-and-cut integer programming solver using the PuLP library. This is typically fast, although
    it can be slow for larger instances."""

    def is_approximate(self) -> bool:
        """
        :return: True if the algorithm is an approximation scheme, or false for exact algorithms.
        """
        return self in (
            PBMultiAlgorithm.GREEDY,
            PBMultiAlgorithm.RATIO_GREEDY,
            PBMultiAlgorithm.BRANCH_AND_BOUND,
            PBMultiAlgorithm.SIMULATED_ANNEALING,
            PBMultiAlgorithm.GENETIC_ALGORITHM
        )


class PBMultiProblem:
    def __init__(self, num_projects: int, num_voters: int, budget: List[int], costs: List[List[int]],
                 utilities: List[List[int]], projects: List[int] = None, voters: List[int] = None):
        """
        Instantiates a multi-dimensional (d-constraint) participatory budgeting problem.

        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param budget: A list of fixed resources or budgets in the instance.
        :param costs: A list of lists denoting the costs of each item towards a resource, i.e., costs[j][p] is the
        cost of project p towards resource j.
        :param utilities: A list of lists of utilities for each voter over the projects, i.e., utilities[v][p] is the
        utility voter v derives from project p.
        :param projects: An optional list of custom project ids, defaulting to 1,...,num_projects otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 1,...,num_voters otherwise.
        """
        self.num_projects: int = num_projects
        self.num_voters: int = num_voters
        self.budget: List[int] = budget
        self.costs: List[List[int]] = costs
        self.utilities: List[List[int]] = utilities
        self.projects: List[int] = projects if projects else [idx for idx in range(num_projects)]
        self.voters: List[int] = voters if voters else [idx for idx in range(num_voters)]

    def __str__(self) -> str:
        """
        :return: A string representing the problem data.
        """
        return str(self.__dict__)

    def solve(self, algorithm: PBMultiAlgorithm) -> PBResult:
        """
        Reduces a multidimensional participatory budgeting problem to the multidimensional knapsack problem
        and solves it using the specified algorithm.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :return: The optimal allocation for the problem, its overall value and the run-time in milliseconds.
        """
        start_time: float = default_timer()

        values: List[int] = pbfunc.aggregate_utilitarian(
            self.num_projects,
            self.utilities,
        )

        allocation = PBResult([], 0, 0.0, algorithm, None)

        if algorithm == PBMultiAlgorithm.BRUTE_FORCE:
            allocation = solvers.multi_brute_force(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.MEMOIZATION:
            allocation = solvers.multi_memoization(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.DYNAMIC_PROGRAMMING:
            allocation = solvers.multi_dynamic_programming(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.BRANCH_AND_BOUND:
            allocation = solvers.multi_branch_and_bound(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.SIMULATED_ANNEALING:
            allocation = solvers.multi_simulated_annealing(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.GENETIC_ALGORITHM:
            allocation = solvers.multi_genetic_algorithm(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.GREEDY:
            allocation = solvers.multi_greedy(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.RATIO_GREEDY:
            allocation = solvers.multi_ratio_greedy(self.budget, self.costs, values)

        elif algorithm == PBMultiAlgorithm.ILP_SOLVER:
            allocation = solvers.multi_integer_programming(self.budget, self.costs, values)

        end_time: float = default_timer()

        return PBResult(
            allocation=pbfunc.resolve_project_ids(
                self.projects,
                allocation[0]
            ),
            value=allocation[1],
            runtime=(end_time - start_time) * 1000,
            algorithm=str(algorithm),
            approximate=algorithm.is_approximate()
        )

    def approximate(self) -> PBResult:
        ratio_greedy: PBResult = self.solve(PBMultiAlgorithm.RATIO_GREEDY)
        simulated_annealing: PBResult = self.solve(PBMultiAlgorithm.SIMULATED_ANNEALING)
        genetic_algorithm: PBResult = self.solve(PBMultiAlgorithm.GENETIC_ALGORITHM)
        return max([ratio_greedy, simulated_annealing, genetic_algorithm], key=lambda r: r.value)
