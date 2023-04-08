from community_knapsack import PBGenerator,\
    PBSingleProblem,\
    PBMultiProblem
from typing import List, Tuple
import pytest


class TestPBGenerator:
    """Ensures the random generation of participatory budgeting instances performs as expected
    and raises helpful errors when an error occurs."""

    generations: List[Tuple[int, int]] = [(10, 20), (0, 0), (0, 5)]

    @pytest.mark.parametrize('generation', generations)
    def test_generate_int(self, generation: Tuple[int, int]):
        """Ensures that integer generation in bounds produces valid results."""
        generator: PBGenerator = PBGenerator()
        assert generation[0] <= generator._generate_int(generation) <= generation[1]

    def test_fail_generate_int(self):
        """Ensures that an error is raised when integer generation receives bad bounds."""
        generator: PBGenerator = PBGenerator()
        with pytest.raises(ValueError):
            generator._generate_int((20, 10))
        with pytest.raises(ValueError):
            generator._generate_int((-10, 20))
        with pytest.raises(ValueError):
            generator._generate_int((10, -20))
        with pytest.raises(ValueError):
            generator._generate_int((-10, -20))

    def test_fail_single_zero_costs(self):
        """Ensures that an error is raised when the costs bounds are non-positive."""
        generator: PBGenerator = PBGenerator()
        with pytest.raises(ValueError):
            generator.generate_single_problem(
                num_projects_bound=(1, 10),
                num_voters_bound=(1, 10),
                budget_bound=(2000, 10_000),
                cost_bound=(0, 3000),
                utility_bound=(0, 1)
            )

    def test_fail_multi_zero_costs(self):
        """Ensures that an error is raised when the costs bounds are non-positive."""
        generator: PBGenerator = PBGenerator()
        with pytest.raises(ValueError):
            generator.generate_multi_problem(
                num_projects_bound=(1, 10),
                num_voters_bound=(1, 10),
                budget_bound=((-2000, 10_000), (10, 50)),
                cost_bound=((100, 3000), (1, 5)),
                utility_bound=(0, 1)
            )

    def test_generate_utilities(self):
        """Ensures that non-uniform utility generation produces the expected results."""
        generator: PBGenerator = PBGenerator(seed=5)
        utilities: List[List[int]] = generator._generate_utilities(5, 5, (0, 1), (1, 3))
        assert utilities == [
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1],
            [0, 1, 0, 0, 0]
        ]

    def test_single_problem_generation(self):
        """Ensures that single problem generation produces the expected result."""
        generator: PBGenerator = PBGenerator(seed=5)
        problem: PBSingleProblem = generator.generate_single_problem(
            num_projects_bound=(1, 10),
            num_voters_bound=(1, 10),
            budget_bound=(2000, 10_000),
            cost_bound=(100, 3000),
            utility_bound=(0, 1)
        )
        assert problem.num_projects == 4
        assert problem.num_voters == 7
        assert problem.budget == 9286
        assert problem.costs == [1524, 2221, 1132, 840]
        assert problem.utilities == [
            [1, 0, 1, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]
        ]

    def test_multi_problem_generation(self):
        """Ensures that multi problem generation produces the expected result."""
        generator: PBGenerator = PBGenerator(seed=5)
        problem: PBMultiProblem = generator.generate_multi_problem(
            num_projects_bound=(1, 10),
            num_voters_bound=(1, 10),
            budget_bound=((2000, 10_000), (10, 50)),
            cost_bound=((100, 3000), (1, 5)),
            utility_bound=(0, 1)
        )
        assert problem.num_projects == 4
        assert problem.num_voters == 7
        assert problem.budget == [9286, 26]
        assert problem.costs == [
            [2221, 1132, 840, 2082],
            [4, 1, 3, 1]
        ]
        assert problem.utilities == [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 1, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]


