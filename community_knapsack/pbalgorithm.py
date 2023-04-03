from .solvers import exact, approximate
from enum import Enum


class _PBAlgorithm(Enum):
    pass


class PBSingleAlgorithm(_PBAlgorithm):

    BRUTE_FORCE = (exact.brute_force,)
    """A very slow but exact algorithm that enumerates every possible allocation and returns the best (optimal) one.
    This is likely too slow and is very rarely applicable."""

    MEMOIZATION = (exact.memoization,)
    """A relatively slow pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster
    result."""

    DYNAMIC_PROGRAMMING = (exact.dynamic_programming,)
    """A relatively slow pseudo-polynomial, exact algorithm that improves upon the brute force algorithm for a faster
    result."""

    BRANCH_AND_BOUND = (exact.branch_and_bound,)
    """An exact algorithm that begins to enumerate every possible allocation but prunes certain branches
    for a faster result. The run-time is exponential (slow) but can be much faster depending on the problem."""

    FPTAS = (approximate.fptas,)
    """A relatively fast algorithm that uses the dynamic programming algorithm to find an approximation within
    50% of the optimal allocation. A very good option for larger problem sizes where exact algorithms are too slow."""

    SIMULATED_ANNEALING = (approximate.simulated_annealing,)
    """A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation."""

    GENETIC_ALGORITHM = (approximate.genetic_algorithm,)
    """A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution."""

    GREEDY = (approximate.greedy,)
    """A fast approximation algorithm that picks projects by their overall value. This is commonly used
    in real-world budget allocations."""

    RATIO_GREEDY = (approximate.ratio_greedy,)
    """A fast and typically better (vs. greedy) approximation algorithm that picks projects by their overall
    value-to-weight ratio."""

    ILP_SOLVER = (exact.integer_programming,)
    """A branch-and-cut integer programming solver using the PuLP library. This is typically fast, although
    it can be slow for larger instances."""

    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)

    def is_approximate(self) -> bool:
        """
        :return: True if the algorithm is an approximation scheme, or false for exact algorithms.
        """
        return self in (
            PBSingleAlgorithm.GREEDY,
            PBSingleAlgorithm.RATIO_GREEDY,
            PBSingleAlgorithm.FPTAS,
            PBSingleAlgorithm.SIMULATED_ANNEALING,
            PBSingleAlgorithm.GENETIC_ALGORITHM
        )


class PBMultiAlgorithm(_PBAlgorithm):
    BRUTE_FORCE = (exact.multi_brute_force,)
    """A very slow but exact algorithm that enumerates every possible allocation and returns the best (optimal) one.
    This is likely too slow and is very rarely applicable."""

    MEMOIZATION = (exact.multi_memoization,)
    """A relatively slow exact algorithm that improves upon the brute force algorithm for a faster result."""

    DYNAMIC_PROGRAMMING = (exact.multi_dynamic_programming,)
    """An exact algorithm that improves upon the brute force algorithm, but is still extremely slow given larger
    problem sizes, especially with multiple dimensions. This is very rarely applicable."""

    BRANCH_AND_BOUND = (approximate.multi_branch_and_bound,)
    """An approximation algorithm that begins to enumerate every possible allocation but prunes 
    certain branches for a faster result. The run-time is exponential (slow) but can be much 
    faster depending on the problem."""

    SIMULATED_ANNEALING = (approximate.multi_simulated_annealing,)
    """A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation."""

    GENETIC_ALGORITHM = (approximate.multi_genetic_algorithm,)
    """A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution."""

    GREEDY = (approximate.greedy,)
    """A fast approximation algorithm that picks projects by their overall value. This is commonly used
    in real-world budget allocations."""

    RATIO_GREEDY = (approximate.multi_ratio_greedy,)
    """A fast and typically better (vs. greedy) approximation algorithm that picks projects by their overall
    value-to-weight ratio, where weight is the sum of all weights for each item."""

    ILP_SOLVER = (exact.multi_integer_programming,)
    """A branch-and-cut integer programming solver using the PuLP library. This is typically fast, although
    it can be slow for larger instances."""

    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)

    def is_approximate(self) -> bool:
        """
        :return: True if the algorithm is an approximation scheme, or false for exact algorithms.
        """
        return self in (
            PBMultiAlgorithm.GREEDY,
            PBMultiAlgorithm.RATIO_GREEDY,
            PBMultiAlgorithm.BRANCH_AND_BOUND,
            PBMultiAlgorithm.SIMULATED_ANNEALING,
            PBMultiAlgorithm.GENETIC_ALGORITHM
        )
