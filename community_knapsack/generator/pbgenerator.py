from community_knapsack import PBSingleProblem, PBMultiProblem
from typing import Sequence, Tuple, List
from random import Random
import warnings


class PBGenerator:
    """Randomly generates a PBSingleProblem or a PBMultiProblem by generating each parameter
    within certain specified bounds. The votes can either be uniformly generated or each
    project can be given some random weighting to simulate `real-world` scenarios in
    which some projects are more popular than others."""

    def __init__(self, seed: int = -1):
        """
        Instantiates a PBGenerator object with an optional seed value (for random generation) for generating
        single and multi-budget participatory budgeting instances.

        :param seed: The random seed used to generate the problems. Use the same seed to obtain the same
        problems.
        """
        self._random = Random()
        if seed != -1:
            self._random.seed(seed)

    def _generate_int(self, bound: Tuple[int, int]) -> int:
        """
        Generates a random integer within a minimum and maximum bound.
        :param bound: The bounds of generation as a tuple (min_bound, max_bound).
        :return: A random integer within the bounds supplied.
        """
        if bound[0] < 0 or bound[1] < 0:
            raise ValueError(f'The bounds ({bound[0]}, {bound[1]}) entered must be positive integers.')
        if bound[0] > bound[1]:
            raise ValueError(f'The lower bound `{bound[0]}` must be less than or '
                             f'equal to the upper bound `{bound[1]}`.')
        return self._random.randint(bound[0], bound[1])

    def _generate_utilities(
            self,
            num_projects: int,
            num_voters: int,
            utility_bound: Tuple[int, int],
            vote_length_bound: Tuple[int, int] = (0, -1)
    ) -> List[List[int]]:
        """
        Generates a random 2-dimensional list of utilities for each voter over each project. Each
        utility over a project is randomly generated within the utility bound.

        :param num_projects: The number of projects to generate utilities for.
        :param num_voters: The number of voters to generate utilities for.
        :param utility_bound: The bounds of possible utilities as a tuple (min_bound, max_bound).
        :param vote_length_bound: The minimum and maximum number of votes each voter can make.
        :return: A two-dimensional list of utilities for each voter over each project.
        """

        if vote_length_bound[0] < 0:
            vote_length_bound = (0, vote_length_bound[1])

        if vote_length_bound[1] < 0:
            vote_length_bound = (vote_length_bound[0], num_projects)

        if utility_bound[0] <= 0:
            utility_bound = (1, utility_bound[1])

        weightings: List[float] = [min(max(self._random.gauss(0.5, 0.2), 0), 1) for _ in range(num_projects)]
        num_votes: int = self._generate_int(vote_length_bound)

        utilities: List[List[int]] = [[0 for _ in range(num_projects)] for _ in range(num_voters)]

        for voter in range(num_voters):
            for selection in self._random.choices(range(num_projects), weightings, k=num_votes):
                utilities[voter][selection] = self._generate_int(utility_bound)

        return utilities

        # weightings: List[float] = [self._random.random() for _ in range(num_projects)]
        # if utility_bound[0] == 0:
        #     utility_bound = (1, utility_bound[1])
        # return [
        #     [
        #         self._generate_int(utility_bound) if self._random.random() < weightings[idx]**2 else 0
        #         for idx in range(num_projects)
        #     ] for _ in range(num_voters)
        # ]

        # return [[self._generate_int(utility_bound) for _ in range(num_projects)] for _ in range(num_voters)]

    def generate_single_problem(
            self,
            num_projects_bound: Tuple[int, int],
            num_voters_bound: Tuple[int, int],
            budget_bound: Tuple[int, int],
            cost_bound: Tuple[int, int],
            utility_bound: Tuple[int, int] = (0, 1),
            vote_length_bound: Tuple[int, int] = (0, -1)
    ) -> PBSingleProblem:
        """
        Creates a PBSingleProblem object containing randomly generated instance data, i.e., a random
        number of projects and voters, a random budget, random costs for each project and random
        utilities all within some specified boundaries.

        :param num_projects_bound: The minimum and maximum possible number of projects.
        :param num_voters_bound: The minimum and maximum possible number of voters.
        :param budget_bound: The minimum and maximum possible budget.
        :param cost_bound: The minimum and maximum cost for each project.
        :param utility_bound: The minimum and maximum utility that each voter derives from each project.
        :param vote_length_bound: The minimum and maximum number of votes each voter can make.
        :return: A PBSingleProblem object containing the randomly generated instance.
        """
        num_projects: int = self._generate_int(num_projects_bound)
        num_voters: int = self._generate_int(num_voters_bound)
        budget: int = self._generate_int(budget_bound)

        if 0 in cost_bound:
            raise ValueError('The cost bound must only contain positive integers to generate instances.')

        costs: List[int] = [self._generate_int(cost_bound) for _ in range(num_projects)]
        utilities: List[List[int]] = self._generate_utilities(
            num_projects,
            num_voters,
            utility_bound,
            vote_length_bound
        )

        return PBSingleProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities
        )

    def generate_multi_problem(
            self,
            num_projects_bound: Tuple[int, int],
            num_voters_bound: Tuple[int, int],
            budget_bound: Sequence[Tuple[int, int]],
            cost_bound: Sequence[Tuple[int, int]],
            utility_bound: Tuple[int, int] = (0, 1),
            vote_length_bound: Tuple[int, int] = (0, -1)
    ) -> PBMultiProblem:
        """
        Creates a PBMultiProblem object containing randomly generated instance data, i.e., a random
        number of projects and voters, random budgets, random costs for each project in each dimension
        (for each budget) and random utilities all within some specified boundaries.

        :param num_projects_bound: The minimum and maximum possible number of projects.
        :param num_voters_bound: The minimum and maximum possible number of voters.
        :param budget_bound: A sequence of minimum and maximum bounds for each budget.
        :param cost_bound: A sequence of minimum and maximum bounds for each project cost for each budget.
        :param utility_bound: The minimum and maximum utility that each voter derives from each project.
        :param vote_length_bound: The minimum and maximum number of votes each voter can make.
        :return: A PBMultiProblem object containing the randomly generated instance.
        """
        num_projects: int = self._generate_int(num_projects_bound)
        num_voters: int = self._generate_int(num_voters_bound)
        budget: List[int] = [
            self._generate_int(budget_bound[dim])
            for dim in range(len(budget_bound))
        ]

        for bound in cost_bound:
            if 0 in bound:
                raise ValueError('The cost bounds must only contain positive integers to generate instances.')

        costs: List[List[int]] = [
            [self._generate_int(cost_bound[dim]) for _ in range(num_projects)]
            for dim in range(len(budget_bound))
        ]
        utilities: List[List[int]] = self._generate_utilities(
            num_projects,
            num_voters,
            utility_bound,
            vote_length_bound
        )

        return PBMultiProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities
        )
