import numpy as np
import pygame
from nn import FeedForwardNetwork


class CellField:
    def __init__(self, cell_size=100, margin=4, zero_color='red', nonzero_color='green'):
        self.values = [[0 for _ in range(3)]
                       for _ in range(3)]
        self.cell_size = (cell_size, cell_size)
        self.margin = margin
        self.zero_color = zero_color
        self.nonzero_color = nonzero_color
        self.font = pygame.freetype.SysFont('freeserif', 100)
        self.network = FeedForwardNetwork(input_num=9,
                                          hidden_layer_nums=[20, 12],
                                          output_num=9)
        
    def draw(self, surface, offset):
        for i in range(3):
            for j in range(3):
                cell_offset = (offset[0] + j * (self.cell_size[0] + self.margin),
                               offset[1] + i * (self.cell_size[1] + self.margin))
                rect = pygame.Rect(cell_offset,
                                   self.cell_size)
                cell_color = self.zero_color if self.values[i][j] == 0 else self.nonzero_color
                pygame.draw.rect(surface, cell_color, rect)

                text_offset = (cell_offset[0] + 30, cell_offset[1] + 15)
                text_surface, _ = self.font.render(str(self.values[i][j]), (0, 0, 0))
                surface.blit(text_surface, text_offset)

    def increment_next_cell(self):
        inputs = []
        for vals in self.values:
            inputs.extend(vals)
        net_input = np.array([inputs])
        net_output = self.network.feed_forward(net_input)

        picked_cell = np.argmax(net_output)
        self.values[picked_cell//3][picked_cell%3] += 1
