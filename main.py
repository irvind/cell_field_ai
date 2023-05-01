# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.pygame.org/docs/
# https://pythonru.com/uroki/biblioteka-pygame-chast-1-vvedenie
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
import numpy as np
import pygame

from cell_field import CellField
from nn import FeedForwardNetwork

FPS = 24
SCREEN_SIZE = (640, 480)


def run():
    pygame.init()
    pygame.freetype.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    running = True
    while running:
        _continue = run_frame(screen, clock)
        if not _continue:
            break

    # print(pygame.font.get_fonts())

    pygame.quit()


def run_frame(screen, clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    screen.fill((255, 255, 255))

    field = CellField()
    offset = ((float(SCREEN_SIZE[0]) / 2) - (field.cell_size[0] * 3 + field.margin * 2) / 2,
              (float(SCREEN_SIZE[1]) / 2) - (field.cell_size[1] * 3 + field.margin * 2) / 2)
    field.draw(screen, offset)

    pygame.display.flip()
    clock.tick(FPS)

    return True


if __name__ == '__main__':
    run()
