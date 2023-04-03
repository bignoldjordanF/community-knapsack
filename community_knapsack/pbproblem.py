from .pbalgorithm import _PBAlgorithm,\
    PBSingleAlgorithm,\
    PBMultiAlgorithm
from .pbresult import PBResult
from . import pbutils

from typing import Sequence, Union, List
from abc import ABC, abstractmethod
from timeit import default_timer
import warnings


class PBProblemError(Exception):
    """An exception raised when an error is encountered instantiating a _PBProblem object."""
    pass


class _PBProblem(ABC):
    """An abstract base class for the PBSingleProblem and PBMultiProblem classes, storing
    their common attributes: projects, voters and utilities."""
    @abstractmethod
    def __init__(
            self,
            num_projects: int,
            num_voters: int,
            utilities: Sequence[Sequence[int]],
            projects: Sequence[Union[str, int]] = None,
            voters: Sequence[Union[str, int]] = None
    ):
        """
        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param utilities: A list of lists of utilities for each voter over the projects.
        :param projects: An optional list of custom project ids, defaulting to 0,...,num_projects-1 otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 0,...,num_voters-1 otherwise.
        """
        # Set Projects & Voters
        if not projects:
            projects = [idx for idx in range(num_projects)]

        if not voters:
            voters = [idx for idx in range(num_voters)]

        # Verify Parameters
        if len(projects) != num_projects:
            warnings.warn(f'An unexpected number of projects {len(projects)} were found.'
                          f'The instance has been updated.')
            num_projects = len(projects)

        if len(voters) != num_voters:
            warnings.warn(f'An unexpected number of voters {len(voters)} were found.'
                          f'The instance has been updated.')
            num_voters = len(voters)

        # This is currently fatal where there must be the expected number of voter utilities,
        # but this may not matter if we are willing to risk 'cutting-off' or 'extending' the
        # number of voters:
        if len(utilities) != num_voters:
            raise PBProblemError(f'There were {len(utilities)} votes (voters) found but {num_voters} expected.')

        for vid, utility in enumerate(utilities):
            if len(utility) != num_projects:
                raise PBProblemError(f'Voter {vid} has utilities for {len(utility)} projects but expected utilities '
                                     f'for {num_projects} projects.')

        self.num_projects = num_projects
        self.num_voters = num_voters
        self.utilities = utilities
        self.projects = projects
        self.voters = voters

    @abstractmethod
    def solve(self, algorithm: _PBAlgorithm):
        pass


class PBSingleProblem(_PBProblem):
    """A class to store and solve single-dimensional (single budget) participatory budgeting problem data."""

    def __init__(
            self,
            num_projects: int,
            num_voters: int,
            budget: int,
            costs: Sequence[int],
            utilities: Sequence[Sequence[int]],
            projects: Sequence[Union[str, int]] = None,
            voters: Sequence[Union[str, int]] = None
    ):
        """
        Instantiates a single-dimensional (a typical single budget) participatory budgeting problem. This is
        the correct class to use if you have a single budget and thus each project has a single cost. If you
        are unsure, use the PBMultiProblem class.

        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param budget: A single fixed budget for the instance (the budget of your instance).
        :param costs: A list of costs for each project, e.g., [10, 12, ...], project one has cost 10, two 12, etc...
        :param utilities: A list of lists of utilities for each voter over the projects.
        :param projects: An optional list of custom project ids, defaulting to 0,...,num_projects-1 otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 0,...,num_voters-1 otherwise.
        """
        # Call Superclass
        super().__init__(num_projects, num_voters, utilities, projects, voters)

        # Verify Parameters
        if self.num_projects != len(costs):
            raise PBProblemError(f'There were {len(costs)} project costs found but {self.num_projects} expected.')

        self.budget = budget
        self.costs = costs

    def solve(self, algorithm: PBSingleAlgorithm):
        """
        Reduces a one-dimensional (single budget) participatory budgeting problem to the classic binary
        knapsack problem and solves it using the specified algorithm, returning a budget allocation.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :return: An allocation for the problem, its overall value and the run-time in milliseconds.
        """
        start_time: float = default_timer()

        # Aggregate the utilities via utilitarian welfare:
        values: List[int] = pbutils.aggregate_utilitarian(
            self.num_projects,
            self.utilities
        )
        allocation, value = algorithm(self.budget, self.costs, values)

        end_time: float = default_timer()

        return PBResult(
            allocation=[self.projects[idx] for idx in allocation],
            value=value,
            runtime=(end_time - start_time) * 1000,
            algorithm=algorithm.name,
            approximate=algorithm.is_approximate()
        )


class PBMultiProblem(_PBProblem):
    """A class to store and solve multi-dimensional (multi-budget) participatory budgeting problem data."""
    def __init__(
            self,
            num_projects: int,
            num_voters: int,
            budget: Sequence[int],
            costs: Sequence[Sequence[int]],
            utilities: Sequence[Sequence[int]],
            projects: Sequence[Union[str, int]] = None,
            voters: Sequence[Union[str, int]] = None
    ):
        """
        Instantiates a multidimensional (a multi-budget) participatory budgeting problem. This is the correct
        class to use if you know that you have multiple (more than one) budgets, and thus each project has
        a cost towards each budget (e.g., if you have three budgets, each project has three costs, one for
        each budget).

        :param num_projects: The number of projects in the instance.
        :param num_voters: The number of voters in the instance.
        :param budget: A list of budgets for the instance, e.g., [10000, 200000, ...].
        :param costs: A list of lists of project costs in each dimension, e.g., [[5000, 6000], [98000, 102000]].
        :param utilities: A list of lists of utilities for each voter over the projects.
        :param projects: An optional list of custom project ids, defaulting to 0,...,num_projects-1 otherwise.
        :param voters: An optional list of custom voter ids, defaulting to 0,...,num_voters-1 otherwise.
        """
        # Call Superclass
        super().__init__(num_projects, num_voters, utilities, projects, voters)

        # Verify Parameters
        if len(budget) != len(costs):
            raise PBProblemError(f'There were {len(budget)} budgets found and {len(costs)} cost dimensions found, '
                                 f'but these should be equal.')

        for dim, cost in enumerate(costs):
            if len(cost) != self.num_projects:
                raise PBProblemError(f'There were {len(cost)} costs found in dimension {dim} but {num_projects} '
                                     f'expected.')

        self.budget = budget
        self.costs = costs

    def solve(self, algorithm: PBMultiAlgorithm):
        """
        Reduces a multidimensional (multiple budget) participatory budgeting problem to the
        multidimensional binary knapsack problem and solves it using the specified algorithm,
        returning a budget allocation.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :return: An allocation for the problem, its overall value and the run-time in milliseconds.
        """
        start_time: float = default_timer()

        # Aggregate the utilities via utilitarian welfare:
        values: List[int] = pbutils.aggregate_utilitarian(
            self.num_projects,
            self.utilities
        )
        allocation, value = algorithm(self.budget, self.costs, values)

        end_time: float = default_timer()

        return PBResult(
            allocation=[self.projects[idx] for idx in allocation],
            value=value,
            runtime=(end_time - start_time) * 1000,
            algorithm=algorithm.name,
            approximate=algorithm.is_approximate()
        )
