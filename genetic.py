import settings
from cell_field import CellField
from errors import EndOfPoupulation


class Population:
    def __init__(self):
        self.individuals = None

    def spawn_initial_population(self) -> None:
        self.individuals = [CellField() for _ in range(settings.INITIAL_POPULATION_SIZE)]

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

    def generate_next_population() -> None:
        # TODO
        pass



