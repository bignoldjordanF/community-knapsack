from . import pbfunc
from . import solvers

from collections import namedtuple
from timeit import default_timer
from typing import List
from enum import Enum


class PBAlgorithm(Enum):
    BRUTE_FORCE = 0
    """A very slow but exact algorithm that enumerates every possible allocation and returns the best (optimal) one."""

    MEMOIZATION = 1
    """A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result."""

    DYNAMIC_PROGRAMMING = 2
    """A pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster result. 
    This is a good option to find an exact solution to a large problem."""

    BRANCH_AND_BOUND = 3
    """A relatively slow algorithm that begins to enumerate every possible allocation but prunes certain searches
    for a faster result. The run-time is exponential (slow) but can be much faster depending on the problem."""

    FPTAS = 4
    """A relatively fast algorithm that uses the dynamic programming algorithm to find an approximation of the
    optimal allocation. A very good option for large problem sizes where exact algorithms are too slow."""

    SIMULATED_ANNEALING = 5
    """A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation."""

    GENETIC_ALGORITHM = 6
    """A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution."""

    def is_approximate(self):
        """
        :return: True if the algorithm is an approximation scheme, or false for exact algorithms.
        """
        return self in (
            PBAlgorithm.FPTAS,
            PBAlgorithm.SIMULATED_ANNEALING,
            PBAlgorithm.GENETIC_ALGORITHM
        )


PBResult = namedtuple('PBResult', ('allocation', 'value', 'runtime', 'algorithm', 'approximation'))
"""A named-tuple for allocation results, containing the allocation as
a list of project ids, its overall value and the runtime in milliseconds."""


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
        :param projects: An optional list of custom project ids, defaulting to 1,...,num_projects otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 1,...,num_voters otherwise.
        """
        self.num_projects: int = num_projects
        self.num_voters: int = num_voters
        self.budget: int = budget
        self.costs: List[int] = costs
        self.utilities: List[List[int]] = utilities
        self.projects: List[int] = projects if projects else [idx + 1 for idx in range(num_projects)]
        self.voters: List[int] = voters if voters else [idx + 1 for idx in range(num_voters)]

    def solve(self, algorithm: PBAlgorithm):
        """
        Reduces a one-dimensional participatory budgeting problem to the one-dimensional knapsack problem
        and solves it using the specified algorithm.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :return: The optimal allocation for the problem, its overall value and the run-time in milliseconds.
        """
        start_time: float = default_timer()

        values: List[int] = pbfunc.aggregate_utilities(
            self.num_projects,
            self.utilities
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

        end_time: float = default_timer()
        return PBResult(
            allocation=pbfunc.resolve_project_ids(
                self.projects,
                allocation[0]
            ),
            value=allocation[1],
            runtime=(end_time - start_time) * 1000,
            algorithm=str(algorithm),
            approximation=algorithm.is_approximate()
        )


class PBMultiAlgorithm(Enum):
    BRUTE_FORCE = 0
    MEMOIZATION = 1
    DYNAMIC_PROGRAMMING = 2
    BRANCH_AND_BOUND = 3
    SIMULATED_ANNEALING = 4
    GENETIC_ALGORITHM = 5


class PBMultiProblem(PBProblem):
    def __init__(self, num_projects: int, num_voters: int, budgets: List[int], costs: List[List[int]],
                 utilities: List[List[int]], projects: List[int] = None, voters: List[int] = None):
        """
        Instantiates a multi-dimensional (d-constraint) participatory budgeting problem.

        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param budgets: A list of fixed resources or budgets in the instance.
        :param costs: A list of lists denoting the costs of each item towards a resource, i.e., costs[j][p] is the
        cost of project p towards resource j.
        :param utilities: A list of lists of utilities for each voter over the projects, i.e., utilities[v][p] is the
        utility voter v derives from project p.
        :param projects: An optional list of custom project ids, defaulting to 1,...,num_projects otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 1,...,num_voters otherwise.
        """
        super().__init__(num_projects, num_voters, 0, [], utilities, projects, voters)
        self.budget: List[int] = budgets
        self.costs: List[List[int]] = costs

    def solve(self, algorithm: PBMultiAlgorithm):
        pass
