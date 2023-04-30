import pygame


class CellField:
    def __init__(self, cell_size=100, margin=4, zero_color='red', nonzero_color='green'):
        self.values = [[2 for _ in range(3)]
                       for _ in range(3)]
        self.cell_size = (cell_size, cell_size)
        self.margin = margin
        self.zero_color = zero_color
        self.nonzero_color = nonzero_color
        self.font = pygame.freetype.SysFont('freeserif', 100)
        
    def draw(self, surface, offset):
        for i in range(3):
            for j in range(3):
                cell_offset = (offset[0] + j * (self.cell_size[0] + self.margin),
                               offset[1] + i * (self.cell_size[1] + self.margin))
                rect = pygame.Rect(cell_offset,
                                   self.cell_size)
                cell_color = self.zero_color if self.values[j][i] == 0 else self.nonzero_color
                pygame.draw.rect(surface, cell_color, rect)

                text_offset = (cell_offset[0] + 30, cell_offset[1] + 15)
                text_surface, _ = self.font.render(str(self.values[j][i]), (0, 0, 0))
                surface.blit(text_surface, text_offset)
