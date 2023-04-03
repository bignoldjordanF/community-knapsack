from dataclasses import dataclass
from typing import List


@dataclass
class PBResult:
    allocation: List[int]
    value: int
    runtime: float
    algorithm: str
    approximate: bool
