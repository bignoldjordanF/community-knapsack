from typing import List, Tuple
import random


def __create_population(num_items: int, population_size: int) -> List[List[int]]:
    return [
        [random.randint(0, 1) for _ in range(num_items)]
        for _ in range(population_size)
    ]


def __selection(
        capacity: int,
        weights: List[int],
        values: List[int],
        population: List[List[int]]
) -> Tuple[List[int], ...]:

    tournament_size: int = 2
    selected: List[List[int]] = []
    for _ in range(2):
        tournament: List[List[int]] = random.sample(population, tournament_size)
        best_chromosome: List[int] = max(
            tournament,
            key=lambda chromosome: __fitness(
                capacity,
                weights,
                values,
                chromosome
            )
        )
        selected.append(best_chromosome)
    return tuple(selected)


def __fitness(
        capacity: int,
        weights: List[int],
        values: List[int],
        chromosome: List[int]
) -> int:
    weight: int = 0
    value: int = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            weight += weights[i]
            value += values[i]

    if weight > capacity:
        return -value

    return value


def __crossover(crossover_rate: float, parent_a: List[int], parent_b: List[int]) -> Tuple[List[int], List[int]]:
    if random.random() > crossover_rate:
        return parent_a, parent_b

    crossover_point: int = random.randint(1, len(parent_a) - 1)
    child_a: List[int] = parent_a[:crossover_point] + parent_b[crossover_point:]
    child_b: List[int] = parent_b[:crossover_point] + parent_a[crossover_point:]

    return child_a, child_b


def __mutation(mutation_rate: float, chromosome: List[int]) -> List[int]:
    if random.random() > mutation_rate:
        return chromosome

    mutation_point: int = random.randint(0, len(chromosome) - 1)
    chromosome[mutation_point] = 1 - chromosome[mutation_point]
    return chromosome


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
    num_items: int = len(values)
    population: List[List[int]] = __create_population(num_items, population_size)

    for i in range(num_generations):
        offspring: List[List[int]] = []

        while len(offspring) < len(population):
            parent_a, parent_b = __selection(capacity, weights, values, population)
            child_a, child_b = __crossover(crossover_rate, parent_a, parent_b)

            child_a = __mutation(mutation_rate, child_a)
            child_b = __mutation(mutation_rate, child_b)

            offspring.append(child_a)
            offspring.append(child_b)

        population = offspring

    best_chromosome: List[int] = max(population, key=lambda chromosome: __fitness(
        capacity,
        weights,
        values,
        chromosome
    ))
    best_fitness: int = __fitness(capacity, weights, values, best_chromosome)

    return [idx for idx, val in enumerate(best_chromosome) if val == 1], best_fitness
