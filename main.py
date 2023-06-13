# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.pygame.org/docs/
# https://pythonru.com/uroki/biblioteka-pygame-chast-1-vvedenie
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
import pygame

from cellfield import GeneticAlgorithm, CellField, settings


def run():
    genetic_algo = GeneticAlgorithm()

    pygame.init()
    pygame.freetype.init()

    screen = pygame.display.set_mode(settings.SCREEN_SIZE)
    clock = pygame.time.Clock()

    genetic_algo.init()
    field = genetic_algo.get_current_individual()

    running = True
    while running:
        _continue = run_frame(screen, clock, field)
        if not _continue:
            break

    # print(pygame.font.get_fonts())

    pygame.quit()


def run_frame(screen: pygame.Surface, clock: pygame.time.Clock, field: CellField):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    screen.fill((255, 255, 255))

    screen_size = settings.SCREEN_SIZE
    offset = ((float(screen_size[0]) / 2) - (field.cell_size[0] * 3 + field.margin * 2) / 2,
              (float(screen_size[1]) / 2) - (field.cell_size[1] * 3 + field.margin * 2) / 2)
    field.draw(screen, offset)

    pygame.display.flip()
    clock.tick(settings.FPS)

    field.increment_next_cell()

    return True


def run2():
    genetic_algo = GeneticAlgorithm()
    genetic_algo.init()
    genetic_algo.simulate_current_population()
    genetic_algo.save_population_result_to_csv('simulation.csv')


if __name__ == '__main__':
    run2()
