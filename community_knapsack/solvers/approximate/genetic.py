from typing import List, Tuple, Callable
import random


def __genetic_algorithm(
        fitness_fn: Callable[[List[int]], int],
        num_items: int,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        num_generations: int
):

    # Population & Chromosome Functions
    def create_population() -> List[List[int]]:
        return [
            [random.randint(0, 1) for _ in range(num_items)]
            for _ in range(population_size)
        ]

    def selection() -> Tuple[List[int], ...]:
        tournament_size: int = 2
        parents: List[List[int]] = []

        for _ in range(2):
            tournament: List[List[int]] = random.sample(population, tournament_size)
            parents.append(max(tournament, key=fitness_fn))

        return tuple(parents)

    def crossover(chromosome_one: List[int], chromosome_two: List[int]) -> Tuple[List[int], List[int]]:
        if random.random() > crossover_rate:
            return chromosome_one, chromosome_two

        crossover_point: int = random.randint(1, len(parent_a) - 1)
        offspring_one: List[int] = chromosome_one[:crossover_point] + chromosome_two[crossover_point:]
        offspring_two: List[int] = chromosome_two[:crossover_point] + chromosome_one[crossover_point:]

        return offspring_one, offspring_two

    def mutate(chromosome: List[int]) -> List[int]:
        if random.random() > mutation_rate:
            return chromosome

        mutation_point: int = random.randint(0, len(chromosome) - 1)
        chromosome[mutation_point] = 1 - chromosome[mutation_point]
        return chromosome

    # Evolutionary Process
    population: List[List[int]] = create_population()
    for _ in range(num_generations):
        offspring: List[List[int]] = []

        while len(offspring) < len(population):
            parent_a, parent_b = selection()
            child_a, child_b = crossover(parent_a, parent_b)

            child_a = mutate(child_a)
            child_b = mutate(child_b)

            offspring.append(child_a)
            offspring.append(child_b)

        population = offspring

    best_chromosome: List[int] = max(population, key=fitness_fn)
    best_fitness: int = fitness_fn(best_chromosome)

    return [idx for idx, val in enumerate(best_chromosome) if val == 1], best_fitness


def genetic_algorithm(
        capacity: int,
        weights: List[int],
        values: List[int],
        population_size: int = 100,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.3,
        num_generations: int = 250
) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm derived from the process of evolution which provides approximations of the
    optimal solution.

    We model allocations as chromosomes, and thus items as genes in these chromosomes. We maintain a
    `population_size` sized population of chromosomes (allocations), and the continually select two
    parent chromosomes and generate offspring through crossover and mutation. At the end of
    the process, the best chromosome in the population is returned.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :param population_size: The number of chromosomes that are maintained in the population.
    :param crossover_rate: The probability of two chromosomes being 'crossed over', i.e., genes mixed.
    :param mutation_rate: The probability of a chromosome being 'mutated', i.e., changing one gene.
    :param num_generations: The number of times that offspring should be created/generated.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    def fitness(chromosome: List[int]) -> int:
        weight: int = 0
        value: int = 0

        # Only add the genes (items) whose bits are one (included):
        for item in range(len(chromosome)):
            if chromosome[item] == 1:
                weight += weights[item]
                value += values[item]

        if weight > capacity:
            return -value

        return value

    num_items: int = len(values)
    return __genetic_algorithm(fitness, num_items, population_size, crossover_rate, mutation_rate, num_generations)


def multi_genetic_algorithm(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int],
        population_size: int = 100,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.3,
        num_generations: int = 250
) -> Tuple[List[int], int]:

    def fitness(chromosome: List[int]) -> int:
        weight: List[int] = [0] * len(capacities)
        value: int = 0

        for item in range(len(chromosome)):
            if chromosome[item] == 1:
                weight = [weight[cid] + weights[cid][item] for cid, _ in enumerate(capacities)]
                value += values[item]

        if any(weight[cid] > capacity for cid, capacity in enumerate(capacities)):
            return -value

        return value

    num_items: int = len(values)
    return __genetic_algorithm(fitness, num_items, population_size, crossover_rate, mutation_rate, num_generations)
