from community_knapsack import PBSingleProblem, PBMultiProblem
from typing import Sequence, Tuple, List
from random import Random


class PBGenerator:
    """Randomly generates a PBSingleProblem or a PBMultiProblem by generating each parameter
    within certain specified bounds. The problems are randomly generated are approval voting
    instances, where each voter approves a random number of projects. This does not generate
    very realistic instances, but is useful for experimentation and evaluation."""

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
            num_voters: int
    ) -> List[List[int]]:
        """
        Generates a random 2-dimensional list of utilities for each voter over each project. Each
        utility over a project is randomly generated within the utility bound.

        :param num_projects: The number of projects to generate utilities for.
        :param num_voters: The number of voters to generate utilities for.
        :return: A two-dimensional list of utilities for each voter over each project.
        """

        utilities: List[List[int]] = []
        probabilities: List[float] = [min(max(self._random.gauss(0.5, 0.2), 0.2), 0.8) for _ in range(num_projects)]

        for voter in range(num_voters):
            utility: List[int] = [0] * num_projects
            for project in range(num_projects):
                if self._random.random() < probabilities[project]:
                    utility[project] = 1
            utilities.append(utility)

        return utilities

    def generate_single_problem(
            self,
            num_projects_bound: Tuple[int, int],
            num_voters_bound: Tuple[int, int],
            budget_bound: Tuple[int, int],
            cost_bound: Tuple[int, int]
    ) -> PBSingleProblem:
        """
        Creates a PBSingleProblem object containing randomly generated instance data, i.e., a random
        number of projects and voters, a random budget, random costs for each project and random
        utilities all within some specified boundaries.

        :param num_projects_bound: The minimum and maximum possible number of projects.
        :param num_voters_bound: The minimum and maximum possible number of voters.
        :param budget_bound: The minimum and maximum possible budget.
        :param cost_bound: The minimum and maximum cost for each project.
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
    ) -> PBMultiProblem:
        """
        Creates a PBMultiProblem object containing randomly generated instance data, i.e., a random
        number of projects and voters, random budgets, random costs for each project in each dimension
        (for each budget) and random utilities all within some specified boundaries.

        :param num_projects_bound: The minimum and maximum possible number of projects.
        :param num_voters_bound: The minimum and maximum possible number of voters.
        :param budget_bound: A sequence of minimum and maximum bounds for each budget.
        :param cost_bound: A sequence of minimum and maximum bounds for each project cost for each budget.
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
        )

        return PBMultiProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities
        )
