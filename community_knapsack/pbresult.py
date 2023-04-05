from dataclasses import dataclass
from typing import List, Union


@dataclass
class PBResult:
    allocation: List[Union[str, int]]
    """A list of project ids (not indexes) that are funded in the budget allocation."""

    value: int
    """The overall value (e.g., number of votes or points in utilitarian) of the allocation -- higher is better."""

    cost: Union[List[int], int]
    """The overall cost(s) of the allocation -- these should not exceed (any of) the budget(s)."""

    runtime: float
    """The overall run-time (i.e. time in milliseconds) of the algorithm."""

    algorithm: str
    """The algorithm used to solve the problem."""

    approximate: bool
    """True if the allocation found is an approximation or if it is exactly correct."""
