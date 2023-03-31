from .pbproblem import PBProblem, PBMultiProblem, _PBBaseProblem
from typing import Union, Tuple, List
import random


def _get_min(pair: Union[Tuple[int, int], int]):
    """The first value of a pair or the exact number if an integer is passed in."""
    return pair[0] if isinstance(pair, Tuple) else pair


def _get_max(pair: Union[Tuple[int, int], int]):
    """The second value of a pair or the exact number if an integer is passed in."""
    return pair[1] if isinstance(pair, Tuple) else pair


class _PBBaseGenerator:
    def __init__(
            self,
            num_projects: Union[Tuple[int, int], int] = (10, 50),
            num_voters: Union[Tuple[int, int], int] = (10, 100),
            utility_bound: Union[Tuple[int, int]] = (0, 1),
    ):
        self._min_projects: int = _get_min(num_projects)
        self._max_projects: int = _get_max(num_projects)

        self._min_voters: int = _get_min(num_voters)
        self._max_voters: int = _get_max(num_voters)

        self._min_utility: int = _get_min(utility_bound)
        self._max_utility: int = _get_max(utility_bound)

    def generate(self) -> _PBBaseProblem:
        projects: int = random.randint(self._min_projects, self._max_projects)
        voters: int = random.randint(self._min_voters, self._max_voters)
        utilities: List[List[int]] = [
            [random.randint(self._min_utility, self._max_utility) for _ in range(projects)]
            for _ in range(voters)
        ]
        return _PBBaseProblem(projects, voters, utilities)


class PBGenerator(_PBBaseGenerator):
    def __init__(
            self,
            num_projects: Union[Tuple[int, int], int] = (10, 50),
            num_voters: Union[Tuple[int, int], int] = (10, 100),
            budget_bound: Union[Tuple[int, int], int] = (500_000, 2_000_000),
            cost_bound: Tuple[int, int] = (50_000, 500_000),
            utility_bound: Union[Tuple[int, int]] = (0, 1)
    ):
        """
        Instantiates a PBGenerator object to generate random PBProblem instances
        with various random data within some minimum and maximum parameters.

        :param num_projects: The number of projects to generate.
        :param num_voters: The number of voters to simulate.
        :param budget_bound: The bounds that the fixed budget should be in.
        :param cost_bound: The bounds that the cost of each project should be in.
        :param utility_bound: The bounds of the utilities voters derive from each project.
        """
        super().__init__(num_projects, num_voters, utility_bound)
        self._min_budget: int = _get_min(budget_bound)
        self._max_budget: int = _get_max(budget_bound)

        self._min_cost: int = _get_min(cost_bound)
        self._max_cost: int = _get_max(cost_bound)

    def generate(self) -> PBProblem:
        """
        :return: A PBProblem object with randomly generated data within certain bounds.
        """
        base: _PBBaseProblem = super().generate()
        budget: int = random.randint(self._min_budget, self._max_budget)
        costs: List[int] = [random.randint(self._min_cost, self._max_cost) for _ in range(base.num_projects)]
        return PBProblem(base.num_projects, base.num_voters, budget, costs, base.utilities)


class PBMultiGenerator(_PBBaseGenerator):
    def __init__(
            self,
            num_projects: Union[Tuple[int, int], int] = (10, 50),
            num_voters: Union[Tuple[int, int], int] = (10, 100),
            budget_bound: Tuple[Union[Tuple[int, int], int], ...] = ((500_000, 2_000_000), (1_000, 5_000)),
            cost_bound: Tuple[Tuple[int, int], ...] = ((50_000, 500_000), (100, 500)),
            utility_bound: Union[Tuple[int, int]] = (0, 1)
    ):
        """
        Instantiates a PBMultiGenerator object to generate random PBMultiProblem
        instances with various random data within some minimum and maximum parameters.

        :param num_projects: The number of projects to generate.
        :param num_voters: The number of voters to simulate.
        :param budget_bound: The bounds that each fixed budget should be in.
        :param cost_bound: The bounds that each cost for each project should be in.
        :param utility_bound: The bounds of the utilities voters derive from each project.
        """
        super().__init__(num_projects, num_voters, utility_bound)
        self._min_budget: List[int] = [_get_min(bound) for bound in budget_bound]
        self._max_budget: List[int] = [_get_max(bound) for bound in budget_bound]

        self._min_cost: List[int] = [_get_min(bound) for bound in cost_bound]
        self._max_cost: List[int] = [_get_max(bound) for bound in cost_bound]

    def generate(self) -> PBMultiProblem:
        """
        :return: A PBMultiProblem object with randomly generated data within certain bounds.
        """
        base: _PBBaseProblem = super().generate()
        budget: List[int] = [
            random.randint(self._min_budget[dim], self._max_budget[dim]) for dim in range(len(self._min_budget))
        ]
        costs: List[List[int]] = [
            [random.randint(self._min_cost[dim], self._max_cost[dim]) for _ in range(base.num_projects)]
            for dim in range(len(self._min_budget))
        ]

        return PBMultiProblem(base.num_projects, base.num_voters, budget, costs, base.utilities)
