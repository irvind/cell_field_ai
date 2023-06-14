import csv
import random
from typing import Optional

from . import settings
from .field import CellField
from .errors import EndOfPoupulation


class Population:
    def __init__(self, individuals: Optional[list[CellField]] = None):
        self.individuals = individuals

    def spawn_initial_population(self) -> None:
        self.individuals = [CellField() for _ in range(settings.POPULATION_SIZE)]

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

        self.phase = 1
        self.cur_individual_idx = 0

    def get_current_individual(self) -> Population:
        return self.population[self.cur_individual_idx]

    def set_next_individual(self) -> None:
        if self.cur_individual_idx + 1 >= len(self.population):
            raise EndOfPoupulation()

        self.cur_individual_idx += 1

    def simulate_current_population(self) -> None:
        for individual in self.population.individuals:
            while not individual.is_finished():
                individual.increment_next_cell()    

    def generate_next_population(self) -> None:
        individuals = self.population.individuals.copy()
        random.shuffle(individuals)

        extended_population_size = settings.POPULATION_SIZE + settings.OFFSPRING_NUMBER
        while len(individuals) < extended_population_size:
            ind1, ind2 = self.select_individuals(num=2)
            # TODO: crossover
            # TODO: mutation
            # TODO: clip
            new_individuals = []
            individuals.extend(new_individuals)

        individuals = self.pick_best_individuals(individuals)

        self.population = Population(individuals)
        self.phase += 1
        self.cur_individual_idx = 0

    @classmethod
    def pick_best_individuals(cls, individuals: list[CellField]) -> list[CellField]:
        # TODO
        pass

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

    def select_individuals(self, num=2 ,tournament_size=2, allow_same=False) -> list[CellField]:
        result = []
        while True:
            for _ in range(num):
                pick = random.choices(self.population.individuals, k=tournament_size)
                best_ind = max(pick, key=lambda v: v.fitness_)
                result.append(best_ind)

            if allow_same:
                break
            same_individuals = all(result[0] == item for item in result)
            if not same_individuals:
                break

        return result
