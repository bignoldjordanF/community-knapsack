import numpy as np
from typing import List, Tuple, Union, Callable
from dataclasses import dataclass
import random


np.seterr(over='ignore')


@dataclass
class Allocation:
    allocation: List[int]
    """An allocation as a list of zeroes (exclusion) and ones (inclusion) where each value represents an item."""

    value: int
    """The overall value of the allocation."""

    weight: int
    """The overall weight of the allocation."""

    def neighbour(self, values: List[int], weights: List[int]) -> 'Allocation':
        """
        Generates a neighbouring allocation by randomly selecting an item (bit) in the current allocation
        and flipping it. If it is currently excluded, it becomes included, and vice versa.

        :param values: A list of values for each item, i.e., values[i] is the value for item i.
        :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
        :return: A neighbouring allocation with one included item excluded or vice versa.
        """
        # Copy the allocation:
        _allocation: List[int] = self.allocation[:]
        _value: int = self.value
        _weight: int = self.weight

        # Flip a random bit in the allocation:
        random_idx: int = random.randint(0, len(_allocation) - 1)
        _allocation[random_idx] = 1 - _allocation[random_idx]

        # Update the values and weights accordingly:
        inc_exc: int = 1 if _allocation[random_idx] else -1
        _value += inc_exc * values[random_idx]
        _weight += inc_exc * weights[random_idx]

        return Allocation(_allocation, _value, _weight)


@dataclass
class MultiAllocation(Allocation):

    weight: List[int]
    """The overall weight of the allocation."""

    def neighbour(self, values: List[int], weights: List[List[int]]) -> 'MultiAllocation':
        """
        Generates a neighbouring allocation by randomly selecting an item (bit) in the current allocation
        and flipping it. If it is currently excluded, it becomes included, and vice versa.

        :param values: A list of values for each item, i.e., values[i] is the value for item i.
        :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
        :return: A neighbouring allocation with one included item excluded or vice versa.
        """
        # Copy the allocation:
        _allocation: List[int] = self.allocation[:]
        _value: int = self.value
        _weight: List[int] = self.weight

        # Flip a random bit in the allocation:
        random_idx: int = random.randint(0, len(_allocation) - 1)
        _allocation[random_idx] = 1 - _allocation[random_idx]

        # Update the values and weights accordingly:
        inc_exc: int = 1 if _allocation[random_idx] else -1
        _value += inc_exc * values[random_idx]
        _weight = [_weight[cid] + (inc_exc * weights[cid][random_idx]) for cid in range(len(_weight))]

        return MultiAllocation(_allocation, _value, _weight)


def __simulated_annealing(
        weights: Union[List[int], List[List[int]]],
        values: List[int],
        initial_allocation: Allocation,
        is_invalid: Callable[[Allocation], bool],
        initial_temperature: float,
        temperature_length: int,
        cooling_ratio: float,
        stopping_temperature: float
) -> Tuple[List[int], int]:
    """
    An internal function to run the simulated annealing process given the weights and values of the problem,
    and initial allocation, a validity function and some simulated annealing parameters.

    :param weights: A list of weights for each item (1D), or a list of weights for each capacity for each item (2D).
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :param initial_allocation: The initial (typically empty) allocation from which to start the annealing process.
    :param is_invalid: A function to check whether an allocation is invalid, i.e., exceeds any capacities.
    :param initial_temperature: A decimal representing the likelihood of worse solutions being accepted.
    :param temperature_length: An integer representing the number of neighbours generated per temperature.
    :param cooling_ratio: A decimal representing how much the temperature is reduced after each TL loops.
    :param stopping_temperature: The temperature at which the process should stop and the best allocation returned.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    # The temperature is the likelihood of worse solutions
    # being accepted, starting at the initial temperature:
    current_temperature: float = initial_temperature

    # The current and best allocations start at the
    # empty allocation:
    current: Allocation = initial_allocation
    best: Allocation = current

    # Keep performing TL loops until the temperature is
    # lower than or equal to the stopping temperature:
    while stopping_temperature < current_temperature:
        for _ in range(temperature_length):

            # Generate a neighbouring allocation and skip it if it
            # is invalid:
            neighbour: Allocation = \
                current.neighbour(values, weights)

            if is_invalid(neighbour):
                continue

            # Immediately accept neighbouring allocations that have
            # a higher value than the current allocation:
            delta_value: int = neighbour.value - current.value
            if delta_value >= 0:
                current = neighbour
                if current.value > best.value:
                    best = current
                continue

            # Accept neighbouring allocations with a lower value
            # with some probability, defined p=e^{-dV/T}:
            q = random.uniform(0, 1)
            p = np.exp(-delta_value / current_temperature)
            if q < p:
                current = neighbour

        # After TL loops, reduce the current temperature to
        # accept fewer 'worse' solutions:
        current_temperature *= cooling_ratio

    # Convert the allocation bits into a list of project indexes of included items:
    return [idx for idx, val in enumerate(best.allocation) if val == 1], best.value


def simulated_annealing(
        capacity: int,
        weights: List[int],
        values: List[int],
        initial_temperature: float = 1.0,
        temperature_length: int = 50_000,
        cooling_ratio: float = 0.9,
        stopping_temperature: float = 0.5
) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation.

    Starting from the empty allocation, neighbouring allocations are generating by randomly including
    an excluded item, or excluding an included item and then compared with the current allocation.
    Neighbours with higher values are immediately accepted, and neighbours with lower values are
    accepted with some decreasing probability. The best allocation found throughout the process
    is stored and returned.

    :param capacity: The fixed capacity or budget for the problem. The allocation weights cannot exceed this number.
    :param weights: A list of weights for each item, i.e., weights[i] is the weight for item i.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :param initial_temperature: A decimal representing the likelihood of worse solutions being accepted.
    :param temperature_length: An integer representing the number of neighbours generated per temperature.
    :param cooling_ratio: A decimal representing how much the temperature is reduced after each TL loops.
    :param stopping_temperature: The temperature at which the process should stop and the best allocation returned.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    # The initial allocation is the empty allocation,
    # and therefore has no value or weight:
    initial: Allocation = Allocation(
        allocation=[0] * len(values),
        value=0,
        weight=0
    )

    # Checks if an allocation exceeds the capacity:
    is_invalid: Callable[[Allocation], bool] = \
        lambda allocation: allocation.weight > capacity

    # Send to annealing function and return result:
    return __simulated_annealing(
        weights,
        values,
        initial,
        is_invalid,
        initial_temperature,
        temperature_length,
        cooling_ratio,
        stopping_temperature
    )


def multi_simulated_annealing(
        capacities: List[int],
        weights: List[List[int]],
        values: List[int],
        initial_temperature: float = 1.0,
        temperature_length: int = 50_000,
        cooling_ratio: float = 0.9,
        stopping_temperature: float = 0.5
) -> Tuple[List[int], int]:
    """
    A relatively fast algorithm derived from the process of annealing in thermodynamics which provides
    approximations of the optimal allocation.

    Starting from the empty allocation, neighbouring allocations are generating by randomly including
    an excluded item, or excluding an included item and then compared with the current allocation.
    Neighbours with higher values are immediately accepted, and neighbours with lower values are
    accepted with some decreasing probability. The best allocation found throughout the process
    is stored and returned.

    :param capacities: The fixed capacities for the problem. The allocation weights cannot exceed these.
    :param weights: A 2D list for each capacity and item, e.g., weights[j][i] is the weight of item i to capacity j.
    :param values: A list of values for each item, i.e., values[i] is the value for item i.
    :param initial_temperature: A decimal representing the likelihood of worse solutions being accepted.
    :param temperature_length: An integer representing the number of neighbours generated per temperature.
    :param cooling_ratio: A decimal representing how much the temperature is reduced after each TL loops.
    :param stopping_temperature: The temperature at which the process should stop and the best allocation returned.
    :return: The best allocation found for the problem as a list of project indexes and its overall value.
    """

    # The initial allocation is the empty allocation,
    # and therefore has no value or weight:
    initial: MultiAllocation = MultiAllocation(
        allocation=[0] * len(values),
        value=0,
        weight=[0] * len(capacities)
    )

    # Checks if an allocation exceeds any of the capacities:
    is_invalid: Callable[[Allocation], bool] = \
        lambda allocation: any(allocation.weight[cid] > capacity for cid, capacity in enumerate(capacities))

    # Send to annealing function and return result:
    return __simulated_annealing(
        weights,
        values,
        initial,
        is_invalid,
        initial_temperature,
        temperature_length,
        cooling_ratio,
        stopping_temperature
    )
