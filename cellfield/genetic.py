import csv
import random
from pprint import pprint
from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.typing import ArrayLike

from . import settings
from .field import CellField
from .errors import EndOfPoupulation


@dataclass
class NNMatrixData:
    w_matrices: list[ArrayLike]
    b_weights: list[ArrayLike]


class Population:
    def __init__(self, individuals: Optional[list[CellField]] = None):
        self.individuals = individuals

    def spawn_initial_population(self) -> None:
        self.individuals = [CellField() for _ in range(settings.POPULATION_SIZE)]

    def get_top_10_individual_data(self):
        individuals = self.individuals.copy()
        individuals.sort(key=lambda v: v.fitness_, reverse=True)
        return [i.to_data_row() for i in individuals[:10]]

    def __getitem__(self, key):
        return self.individuals[key]

    def __len__(self):
        return len(self.individuals)


class GeneticAlgorithm:
    def __init__(self, max_phase_num: int = 100):
        self.max_phase_num = max_phase_num
        self.population = None
        self.phase = None
        self.cur_individual_idx = None

    def init(self) -> None:
        self.population = Population()
        self.population.spawn_initial_population()
        self.simulate_current_population()

        self.phase = 1
        self.cur_individual_idx = 0

    def find_best_individual(self, iteration_count: int = 200) -> CellField:
        for iter_idx in range(iteration_count):
            self.generate_next_population()
            print(f'iter_idx: {iter_idx}')
            pprint(self.population.get_top_10_individual_data())

        individuals = self.population.individuals.copy()
        individuals.sort(key=lambda v: v.fitness_, reverse=True)
        return individuals[0]

    def get_current_individual(self) -> Population:
        return self.population[self.cur_individual_idx]

    def set_next_individual(self) -> None:
        if self.cur_individual_idx + 1 >= len(self.population):
            raise EndOfPoupulation()

        self.cur_individual_idx += 1

    def simulate_current_population(self) -> None:
        for individual in self.population.individuals:
            self.simulate_individual(individual)

    def simulate_individual(self, individual: CellField) -> None:
        while not individual.is_finished():
            individual.increment_next_cell()
        individual.calc_fitness()

    def generate_next_population(self) -> None:
        individuals = self.population.individuals.copy()
        random.shuffle(individuals)

        extended_population_size = settings.POPULATION_SIZE + settings.OFFSPRING_NUMBER
        while len(individuals) < extended_population_size:
            individuals.extend(self._generate_new_individuals())

        for individual in individuals:
            self.simulate_individual(individual)

        individuals = self.pick_best_individuals(individuals)

        self.population = Population(individuals)
        self.phase += 1
        self.cur_individual_idx = 0

    def _generate_new_individuals(self):
        ind1_w_matricies, ind2_w_matricies = [], []
        ind1_b_vecs, ind2_b_vecs = [], []
        ind1, ind2 = self.select_individuals(self.population, num=2)
        for i in range(ind1.network.layer_count - 1):
            ind1_mutate_matr, ind1_mutate_b, ind2_mutate_matr, ind2_mutate_b =\
                self._build_matricies(ind1, ind2, i)
            ind1_w_matricies.append(ind1_mutate_matr)
            ind1_b_vecs.append(ind1_mutate_b)
            ind2_w_matricies.append(ind2_mutate_matr)
            ind2_b_vecs.append(ind2_mutate_b)

        new_individuals = (CellField(nn_w_matrices=ind1_w_matricies, nn_b_weights=ind1_b_vecs),
                           CellField(nn_w_matrices=ind2_w_matricies, nn_b_weights=ind2_b_vecs))
        return new_individuals

    def _build_matricies(self, ind1: CellField, ind2: CellField, idx: int):
        ind1_matr = ind1.network.w_matrices[idx]
        ind2_matr = ind2.network.w_matrices[idx]

        ind1_crossover_matr, ind2_crossover_matr =\
            self.crossover(ind1_matr, ind2_matr)
        ind1_mutate_matr = self.mutate(ind1_crossover_matr,
                                        mutate_prob=settings.MUTATION_PROBABILITY)
        ind2_mutate_matr = self.mutate(ind2_crossover_matr,
                                        mutate_prob=settings.MUTATION_PROBABILITY)

        ind1_b = ind1.network.b_weights[idx]
        ind2_b = ind2.network.b_weights[idx]
        ind1_crossover_b, ind2_crossover_b =\
            self.crossover(ind1_b, ind2_b)
        ind1_mutate_b = self.mutate(ind1_crossover_b,
                                    mutate_prob=settings.MUTATION_PROBABILITY)
        ind2_mutate_b = self.mutate(ind2_crossover_b,
                                    mutate_prob=settings.MUTATION_PROBABILITY)

        return (ind1_mutate_matr, ind1_mutate_b, ind2_mutate_matr, ind2_mutate_b)

    @classmethod
    def pick_best_individuals(cls, individuals: list[CellField]) -> list[CellField]:
        individuals = individuals.copy()
        individuals.sort(key=lambda v: v.fitness_, reverse=True)
        return individuals[:settings.POPULATION_SIZE]

    def save_population_result_to_csv(self, csv_filename):
        individuals = self.population.individuals
        rows = [individual.to_data_row() for individual in individuals]
        rows.sort(key=lambda r: r[-1], reverse=True)
        with open(csv_filename, 'w', newline='') as csvfile:
            writter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header_row = [f's{i}{j}' for i in range(3) for j in range(3)]
            header_row.append('fitness')
            writter.writerow(header_row)
            for row in rows:
                writter.writerow(row)

    def select_individuals(self,
                           population: Population,
                           num: int = 2,
                           tournament_size: int = 2,
                           allow_same: bool = False) -> list[CellField]:
        while True:
            result = []
            for _ in range(num):
                pick = random.choices(population.individuals, k=tournament_size)
                best_ind = max(pick, key=lambda v: v.fitness_)
                result.append(best_ind)

            if allow_same:
                break
            same_individuals = all(result[0] == item for item in result)
            if not same_individuals:
                break

        return result

    def crossover(self, p_matr1: ArrayLike, p_matr2: ArrayLike) -> tuple[ArrayLike, ArrayLike]:
        p_matr1_flat = p_matr1.flatten()
        off_matr1_flat = p_matr1_flat.copy()
        p_matr2_flat = p_matr2.flatten()
        off_matr2_flat = p_matr2_flat.copy()
        split_point = np.random.randint(0, len(p_matr1_flat))

        off_matr1_flat[:split_point] = p_matr2_flat[:split_point]
        off_matr2_flat[:split_point] = p_matr1_flat[:split_point]

        orig_shape = p_matr1.shape
        off_matr1 = off_matr1_flat.reshape(orig_shape)
        off_matr2 = off_matr2_flat.reshape(orig_shape)

        return off_matr1, off_matr2

    def mutate(self, off_matr: ArrayLike, mutate_prob: float) -> ArrayLike:
        off_matr = off_matr.copy()
        mutation_flags = np.random.random(off_matr.shape) < mutate_prob
        mutation_values = np.random.uniform(-1, 1, size=off_matr.shape)
        off_matr[mutation_flags] = mutation_values[mutation_flags]

        return off_matr
