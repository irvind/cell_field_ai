from cellfield import GeneticAlgorithm


def run():
    genetic_algo = GeneticAlgorithm()
    genetic_algo.init()
    best_individual = genetic_algo.find_best_individual(iteration_count=2000)
    print('Best individual:')
    print(best_individual.to_data_row())


if __name__ == '__main__':
    run()
