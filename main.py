# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.pygame.org/docs/
# https://pythonru.com/uroki/biblioteka-pygame-chast-1-vvedenie
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
import pygame

from cell_field import CellField

FPS = 1
SCREEN_SIZE = (640, 480)


def run():
    pygame.init()
    pygame.freetype.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    field = CellField()

    running = True
    while running:
        _continue = run_frame(screen, clock, field)
        if not _continue:
            break

    # print(pygame.font.get_fonts())

    pygame.quit()


def run_frame(screen, clock, field):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    screen.fill((255, 255, 255))

    offset = ((float(SCREEN_SIZE[0]) / 2) - (field.cell_size[0] * 3 + field.margin * 2) / 2,
              (float(SCREEN_SIZE[1]) / 2) - (field.cell_size[1] * 3 + field.margin * 2) / 2)
    field.draw(screen, offset)

    pygame.display.flip()
    clock.tick(FPS)

    field.increment_next_cell()

    return True


if __name__ == '__main__':
    run()
