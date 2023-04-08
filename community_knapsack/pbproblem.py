from .pbalgorithm import _PBAlgorithm,\
    PBSingleAlgorithm,\
    PBMultiAlgorithm
from .pbresult import PBResult
from . import pbutils

from typing import Sequence, Union, List
from abc import ABC, abstractmethod
from timeit import default_timer
import multiprocessing as mp
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

        self.num_projects: int = num_projects
        self.num_voters: int = num_voters
        self.utilities: Sequence[Sequence[int]] = utilities
        self.projects: Sequence[Union[str, int]] = projects
        self.voters: Sequence[Union[str, int]] = voters

        # Aggregate the utilities via utilitarian welfare:
        self.values: List[int] = []
        self.update_values()

    def update_values(self):
        # Aggregate the utilities via utilitarian welfare:
        self.values = pbutils.aggregate_utilitarian(
            self.num_projects,
            self.utilities
        )

    @abstractmethod
    def _worker(self, algorithm: _PBAlgorithm, values: List[int], result_queue: mp.Queue) -> None:
        pass

    @abstractmethod
    def solve(self, algorithm: _PBAlgorithm, timeout: float) -> PBResult:
        """
        Reduces a participatory budgeting problem to a binary knapsack problem and solves it using
        the specified algorithm, returning a budget allocation.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :param timeout: The maximum number of seconds before the algorithm aborts, or -1 for no timeout.
        :return: An allocation for the problem, its overall value and the run-time in milliseconds.
        """
        if self.num_projects == 0:
            return PBResult([], 0, 0, 0.0, algorithm.name, algorithm.is_approximate())

        start_time: float = default_timer()

        # Create multiprocessing queue to receive allocation:
        result_queue: mp.Queue = mp.Queue()

        # Start the algorithm process and wait until the timeout is reached:
        process: mp.Process = mp.Process(target=self._worker, args=(algorithm, self.values, result_queue))
        process.start()
        process.join(timeout if timeout >= 0 else None)

        # Terminate the process if it is still running and return the empty allocation:
        if process.is_alive():
            process.terminate()
            warnings.warn(f'The {algorithm.name} algorithm did not finish within the {timeout} second timeout limit. '
                          f'Try increasing the timeout or using a different algorithm (such as an approximation '
                          f'scheme).')
            return PBResult([], 0, 0, timeout, algorithm.name, algorithm.is_approximate())

        # Otherwise, obtain the result from the result queue:
        allocation, value, cost = result_queue.get()
        result_queue.close()

        end_time: float = default_timer()

        return PBResult(
            allocation=[self.projects[idx] for idx in allocation],
            value=value,
            cost=cost,
            runtime=(end_time - start_time) * 1000,
            algorithm=algorithm.name,
            approximate=algorithm.is_approximate()
        )


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

        for pid, cost in enumerate(costs):
            if cost <= 0:
                raise PBProblemError(f'The cost of project {pid} was {cost} but must be a positive integer.')

        self.budget: int = budget
        self.costs: Sequence[int] = costs

    def _worker(self, algorithm: PBSingleAlgorithm, values: List[int], result_queue: mp.Queue) -> None:
        """
        A worker function to call a solver (algorithm) and return the budget allocation for
        the participatory budgeting problem.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :param values: A list of values for each project, i.e., values[i] is the value for project i.
        :param result_queue: A result queue used to store the results from the solver.
        """
        allocation, value = algorithm(self.budget, self.costs, values)
        result_queue.put((allocation, value, sum(
            self.costs[idx] for idx in allocation
        )))

    def solve(self, algorithm: PBSingleAlgorithm, timeout: float = -1) -> PBResult:
        """
        Reduces a one-dimensional (single budget) participatory budgeting problem to the classic binary
        knapsack problem and solves it using the specified algorithm, returning a budget allocation.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :param timeout: The maximum number of seconds before the algorithm aborts, or -1 for no timeout.
        :return: An allocation for the problem, its overall value and the run-time in milliseconds.
        """
        return super().solve(algorithm, timeout)


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
            for pid, p_cost in enumerate(cost):
                if p_cost <= 0:
                    raise PBProblemError(f'The cost of project {pid} was {p_cost} but must be a positive integer.')

        self.budget: Sequence[int] = budget
        self.costs: Sequence[Sequence[int]] = costs

    def _worker(self, algorithm: PBMultiAlgorithm, values: List[int], result_queue: mp.Queue) -> None:
        """
        A worker function to call a solver (algorithm) and return the budget allocation for
        the participatory budgeting problem.

        :param algorithm: The name of the algorithm that should be used to solve the problem.
        :param values: A list of values for each project, i.e., values[i] is the value for project i.
        :param result_queue: A result queue used to store the results from the solver.
        """
        allocation, value = algorithm(self.budget, self.costs, values)
        result_queue.put((allocation, value, [
            sum(self.costs[dim][idx] for idx in allocation) for dim in range(len(self.budget))
        ]))

    def solve(self, multi_algorithm: PBMultiAlgorithm, timeout: float = -1) -> PBResult:
        """
        Reduces a multidimensional (multiple budget) participatory budgeting problem to the
        multidimensional binary knapsack problem and solves it using the specified algorithm,
        returning a budget allocation.

        :param multi_algorithm: The name of the algorithm that should be used to solve the problem.
        :param timeout: The maximum number of seconds before the algorithm aborts, or -1 for no timeout.
        :return: An allocation for the problem, its overall value and the run-time in milliseconds.
        """
        return super().solve(multi_algorithm, timeout)
