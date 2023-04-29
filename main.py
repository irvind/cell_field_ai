# https://coderslegacy.com/python/python-pygame-tutorial/
# https://www.pygame.org/docs/
# https://pythonru.com/uroki/biblioteka-pygame-chast-1-vvedenie
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
import pygame


FPS = 60


def run():  	
    pygame.init()

    screen = pygame.display.set_mode((400,600))
    clock = pygame.time.Clock()

    running = True
    while running:
        _continue = run_frame(screen, clock)
        if not _continue:
            break

    pygame.quit()


def run_frame(screen, clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    screen.fill((255, 255, 255))
    
    offset = (50, 50)
    cell_size = (20, 20)
    margin = 3
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(
                (offset[0] + j * (cell_size[0] + margin),
                 offset[1] + i * (cell_size[1] + margin)),
                cell_size)
            pygame.draw.rect(screen, "red", rect)

    # pygame.draw.circle(screen,
    #                    "red",
    #                    pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),
    #                    40)

    pygame.display.flip()
    clock.tick(FPS)

    return True


if __name__ == '__main__':
    run()
