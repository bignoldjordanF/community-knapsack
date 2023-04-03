from community_knapsack import PBSingleProblem, PBMultiProblem
from typing import Sequence, Tuple, List
from random import Random


class PBGenerator:
    """Randomly generates a PBSingleProblem or a PBMultiProblem by generating each parameter
    within certain specified bounds. The votes can either be uniformly generated or each
    project can be given some random weighting to simulate `real-world` scenarios in
    which some projects are more popular than others."""

    def __init__(self, seed: int = -1):
        """

        :param seed:
        """
        self._random = Random()
        if seed != -1:
            self._random.seed(seed)

    def _generate_int(self, bound: Tuple[int, int]):
        """

        :param bound:
        :return:
        """
        if bound[0] > bound[1]:
            raise ValueError(f'The lower bound `{bound[0]}` must be less than or '
                             f'equal to the upper bound `{bound[1]}`.')
        return self._random.randint(bound[0], bound[1])

    def _generate_utilities(
            self,
            num_projects: int,
            num_voters: int,
            utility_bound: Tuple[int, int],
            non_uniform: bool
    ) -> List[List[int]]:
        """

        :param num_projects:
        :param num_voters:
        :param utility_bound:
        :param non_uniform:
        :return:
        """
        # TODO: Add non-uniform utilities!
        return [[self._generate_int(utility_bound) for _ in range(num_projects)] for _ in range(num_voters)]

    def generate_single_problem(
            self,
            num_projects_bound: Tuple[int, int],
            num_voters_bound: Tuple[int, int],
            budget_bound: Tuple[int, int],
            cost_bound: Tuple[int, int],
            utility_bound: Tuple[int, int] = (0, 1),
            non_uniform: bool = False,
    ) -> PBSingleProblem:
        """

        :param num_projects_bound:
        :param num_voters_bound:
        :param budget_bound:
        :param cost_bound:
        :param utility_bound:
        :param non_uniform:
        :return:
        """
        num_projects: int = self._generate_int(num_projects_bound)
        num_voters: int = self._generate_int(num_voters_bound)
        budget: int = self._generate_int(budget_bound)
        costs: List[int] = [self._generate_int(cost_bound) for _ in range(num_projects)]
        utilities: List[List[int]] = self._generate_utilities(num_projects, num_voters, utility_bound, non_uniform)

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
            non_uniform: bool = False
    ) -> PBMultiProblem:
        """

        :param num_projects_bound:
        :param num_voters_bound:
        :param budget_bound:
        :param cost_bound:
        :param utility_bound:
        :param non_uniform:
        :return:
        """
        num_projects: int = self._generate_int(num_projects_bound)
        num_voters: int = self._generate_int(num_voters_bound)
        budget: List[int] = [
            self._generate_int(budget_bound[dim])
            for dim in range(len(budget_bound))
        ]
        costs: List[List[int]] = [
            [self._generate_int(cost_bound[dim]) for _ in range(num_projects)]
            for dim in range(len(budget_bound))
        ]
        utilities: List[List[int]] = self._generate_utilities(num_projects, num_voters, utility_bound, non_uniform)

        return PBMultiProblem(
            num_projects=num_projects,
            num_voters=num_voters,
            budget=budget,
            costs=costs,
            utilities=utilities
        )
