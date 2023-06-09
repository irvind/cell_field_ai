from typing import Optional
import numpy as np
from numpy.typing import ArrayLike

from .nn import FeedForwardNetwork
from . import settings


class CellField:
    def __init__(self,
                 cell_size: int = 100,
                 margin: int = 4,
                 zero_color: str = 'red',
                 nonzero_color: str = 'green',
                 nn_w_matrices: Optional[list[ArrayLike]] = None,
                 nn_b_weights: Optional[list[ArrayLike]] = None):
        self.values = [[0 for _ in range(3)]
                       for _ in range(3)]
        self.cell_size = (cell_size, cell_size)
        self.margin = margin
        self.zero_color = zero_color
        self.nonzero_color = nonzero_color
        self.fitness_ = None
        self.network = FeedForwardNetwork(input_num=9,
                                          hidden_layer_nums=settings.HIDDEN_LAYERS,
                                          output_num=9,
                                          w_matrices=nn_w_matrices,
                                          b_weights=nn_b_weights)

    def increment_next_cell(self) -> None:
        inputs = []
        for vals in self.values:
            inputs.extend(vals)
        net_input = np.array([inputs])
        net_output = self.network.feed_forward(net_input)

        picked_cell = np.argmax(net_output)
        self.values[picked_cell//3][picked_cell%3] += 1

    def calc_fitness(self) -> float:
        if self.fitness_ is not None:
            return self.fitness_

        vals = np.array(self.values).flatten()
        null_indices = vals == 0
        vals = vals.astype(float)
        vals[null_indices] = np.inf
        self.fitness_ = (1 / vals).sum()

        if not any(null_indices):
            self.fitness_ += 100

        return self.fitness_

    def get_number_of_turns(self) -> int:
        return np.array(self.values).flatten().sum()

    def is_finished(self) -> bool:
        vals = np.array(self.values).flatten()
        return all(vals != 0) or any(vals > 9)

    def to_data_row(self):
        li = []
        for r in self.values:
            li.extend(r)
        li.append(self.calc_fitness())

        return tuple(li)
