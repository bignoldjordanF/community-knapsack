from typing import List, Tuple, Callable
import random


def __genetic_algorithm(
        fitness_fn: Callable[[List[int]], int],
        num_projects: int,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        num_generations: int
):
    """
    An internal function to run the genetic algorithm process given the number of projects, a function
    to compute the fitness of a chromosome and some genetic algorithm parameters.

    :param fitness_fn: A function computing the fitness (value) of a chromosome.
    :param num_projects: The number of projects in the problem.
    :param population_size: The number of chromosomes that are maintained in the population.
    :param crossover_rate: The probability of two chromosomes being 'crossed over', i.e., genes mixed.
    :param mutation_rate: The probability of a chromosome being 'mutated', i.e., changing one gene.
    :param num_generations: The number of times that offspring should be created/generated.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    # Population & Chromosome Functions
    def create_population() -> List[List[int]]:
        """Generates an initial population of `population_size` `num_projects`-sized chromosomes,
        where genes are randomly generated bits (0 or 1) representing project inclusion/exclusion."""
        # We initialise the first chromosome as the empty allocation in case
        # we generate lots of invalid allocations:
        return [
            [0 for _ in range(num_projects)]
            for _ in range(population_size)
        ]

    def selection() -> Tuple[List[int], ...]:
        """Selects two suitable (fit) chromosomes for reproduction via a tournament selection."""
        tournament_size: int = 2
        parents: List[List[int]] = []

        for _ in range(2):
            # Randomly generate a tournament (a 2-subset of the population), and append
            # the one with the highest fitness (value):
            tournament: List[List[int]] = random.sample(population, tournament_size)
            parents.append(max(tournament, key=fitness_fn))

        return tuple(parents)

    def crossover(chromosome_one: List[int], chromosome_two: List[int]) -> Tuple[List[int], List[int]]:
        """Crosses two chromosomes over with some probability by selecting a crossover point and
        swapping the genes of the chromosomes after that point."""
        if random.random() > crossover_rate:
            return chromosome_one, chromosome_two

        crossover_point: int = random.randint(1, len(parent_a) - 1)
        offspring_one: List[int] = chromosome_one[:crossover_point] + chromosome_two[crossover_point:]
        offspring_two: List[int] = chromosome_two[:crossover_point] + chromosome_one[crossover_point:]

        return offspring_one, offspring_two

    def mutate(chromosome: List[int]) -> List[int]:
        """Mutates a chromosome with some probability by flipping a random bit, i.e., including
        an excluded project or vice versa."""
        if random.random() > mutation_rate:
            return chromosome

        mutation_point: int = random.randint(0, len(chromosome) - 1)
        chromosome[mutation_point] = 1 - chromosome[mutation_point]
        return chromosome

    # Evolutionary Process
    population: List[List[int]] = create_population()

    # Create offspring `num_generations` times:
    for i in range(num_generations):
        offspring: List[List[int]] = []

        # Generate as many offspring as there are chromosomes
        # in the population:
        while len(offspring) < len(population):
            # Select parents, generate offspring and mutate:
            parent_a, parent_b = selection()
            child_a, child_b = crossover(parent_a, parent_b)

            child_a = mutate(child_a)
            child_b = mutate(child_b)

            offspring.append(child_a)
            offspring.append(child_b)

        # At the end of each generation, the offspring
        # becomes the population:
        population = offspring

    # The best solution found is in the population after
    # `num_generations` generations:
    best_chromosome: List[int] = max(population, key=fitness_fn)
    best_fitness: int = fitness_fn(best_chromosome)

    if best_fitness == 0:
        return [], 0

    return [idx for idx, val in enumerate(best_chromosome) if val == 1], best_fitness


def genetic_algorithm(
        budget: int,
        costs: List[int],
        values: List[int],
        population_size: int = 200,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.3,
        num_generations: int = 100
) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution.

    Allocations are modelled as chromosomes, and projects as genes in these chromosomes. We maintain a
    `population_size` sized population of chromosomes (allocations), and the continually select two
    parent chromosomes and generate offspring through crossover and mutation. At the end of
    the process, the best chromosome in the population is returned.

    :param budget: The fixed budget for the problem. The allocation costs cannot exceed this number.
    :param costs: A list of costs for each project, i.e., costs[i] is the cost for project i.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :param population_size: The number of chromosomes that are maintained in the population.
    :param crossover_rate: The probability of two chromosomes being 'crossed over', i.e., genes mixed.
    :param mutation_rate: The probability of a chromosome being 'mutated', i.e., changing one gene.
    :param num_generations: The number of times that offspring should be created/generated.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    def fitness(chromosome: List[int]) -> int:
        """Computes the fitness (value) of a chromosome by summing the values of genes (projects)
        with a value of 1. Chromosomes who exceed the cost budget are given a negative
        fitness as they are not suitable for reproduction. """

        cost: int = 0
        value: int = 0

        # Only add the genes (projects) whose bits are one (included):
        for project in range(len(chromosome)):
            if chromosome[project] == 1:
                cost += costs[project]
                value += values[project]

        # Give chromosomes exceeding the budget zero fitness:
        if cost > budget:
            return 0

        return value

    num_projects: int = len(values)
    return __genetic_algorithm(fitness, num_projects, population_size, crossover_rate, mutation_rate, num_generations)


def multi_genetic_algorithm(
        budgets: List[int],
        costs: List[List[int]],
        values: List[int],
        population_size: int = 200,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.3,
        num_generations: int = 100
) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution.

    Allocations are modelled as chromosomes, and projects as genes in these chromosomes. We maintain a
    `population_size` sized population of chromosomes (allocations), and the continually select two
    parent chromosomes and generate offspring through crossover and mutation. At the end of
    the process, the best chromosome in the population is returned.

    :param budgets: The fixed budgets for the problem. The allocation costs cannot exceed these.
    :param costs: A 2D list for each budget and project, e.g., costs[j][i] is the cost of project i to budget j.
    :param values: A list of values for each project, i.e., values[i] is the value for project i.
    :param population_size: The number of chromosomes that are maintained in the population.
    :param crossover_rate: The probability of two chromosomes being 'crossed over', i.e., genes mixed.
    :param mutation_rate: The probability of a chromosome being 'mutated', i.e., changing one gene.
    :param num_generations: The number of times that offspring should be created/generated.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    def fitness(chromosome: List[int]) -> int:
        """Computes the fitness (value) of a chromosome by summing the values of genes (projects)
        with a value of 1. Chromosomes who exceed *any* of the budgets are given a negative
        fitness as they are not suitable for reproduction."""

        cost: List[int] = [0] * len(budgets)
        value: int = 0

        # Only add the genes (projects) whose bits are one (included):
        for project in range(len(chromosome)):
            if chromosome[project] == 1:
                cost = [cost[cid] + costs[cid][project] for cid, _ in enumerate(budgets)]
                value += values[project]

        # Give chromosomes exceeding any budget zero fitness:
        if any(cost[cid] > budget for cid, budget in enumerate(budgets)):
            return 0

        return value

    num_projects: int = len(values)
    return __genetic_algorithm(fitness, num_projects, population_size, crossover_rate, mutation_rate, num_generations)
