from .pbproblem import PBProblem, PBMultiProblem, _PBBaseProblem
from typing import Union, Tuple, List
import random
from abc import ABC, abstractmethod


def _get_min(pair):
    return pair[0] if isinstance(pair, Tuple) else pair


def _get_max(pair):
    return pair[1] if isinstance(pair, Tuple) else pair


class _PBBaseGenerator(ABC):
    @abstractmethod
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

    @abstractmethod
    def generate(self) -> _PBBaseProblem:
        pass


class PBGenerator(_PBBaseGenerator):
    def __init__(
            self,
            num_projects: Union[Tuple[int, int], int] = (10, 50),
            num_voters: Union[Tuple[int, int], int] = (10, 100),
            budget_bound: Union[Tuple[int, int], int] = (500_000, 2_000_000),
            cost_bound: Tuple[int, int] = (50_000, 500_000),
            utility_bound: Union[Tuple[int, int]] = (0, 1)
    ):
        super().__init__(num_projects, num_voters, utility_bound)
        self._min_budget: int = _get_min(budget_bound)
        self._max_budget: int = _get_max(budget_bound)

        self._min_cost: int = _get_min(cost_bound)
        self._max_cost: int = _get_max(cost_bound)

    def generate(self) -> PBProblem:
        projects: int = random.randint(self._min_projects, self._max_projects)
        voters: int = random.randint(self._min_voters, self._max_voters)
        budget: int = random.randint(self._min_budget, self._max_budget)
        costs: List[int] = [random.randint(self._min_cost, self._max_cost) for _ in range(projects)]
        utilities: List[List[int]] = [
            [random.randint(self._min_utility, self._max_utility) for _ in range(projects)]
            for _ in range(voters)
        ]
        return PBProblem(projects, voters, budget, costs, utilities)


class PBMultiGenerator(_PBBaseGenerator):
    def __init__(
            self,
            num_projects: Union[Tuple[int, int], int] = (10, 50),
            num_voters: Union[Tuple[int, int], int] = (10, 100),
            budget_bound: Tuple[Union[Tuple[int, int], int], ...] = ((500_000, 2_000_000), (1_000, 5_000)),
            cost_bound: Tuple[Tuple[int, int], ...] = ((50_000, 500_000), (100, 500)),
            utility_bound: Union[Tuple[int, int]] = (0, 1)
    ):
        super().__init__(num_projects, num_voters, utility_bound)
        self._min_budget: List[int] = [_get_min(bound) for bound in budget_bound]
        self._max_budget: List[int] = [_get_max(bound) for bound in budget_bound]

        self._min_cost: List[int] = [_get_min(bound) for bound in cost_bound]
        self._max_cost: List[int] = [_get_max(bound) for bound in cost_bound]

    def generate(self) -> PBMultiProblem:
        projects: int = random.randint(self._min_projects, self._max_projects)
        voters: int = random.randint(self._min_voters, self._max_voters)
        budget: List[int] = [
            random.randint(self._min_budget[dim], self._max_budget[dim]) for dim in range(len(self._min_budget))
        ]
        costs: List[List[int]] = [
            [random.randint(self._min_cost[dim], self._max_cost[dim]) for _ in range(projects)]
            for dim in range(len(self._min_budget))
        ]
        utilities: List[List[int]] = [
            [random.randint(self._min_utility, self._max_utility) for _ in range(projects)]
            for _ in range(voters)
        ]

        return PBMultiProblem(projects, voters, budget, costs, utilities)
