from typing import List, Optional
import numpy as np


class FeedForwardNetwork:
    def __init__(self,
                 input_num: int,
                 hidden_layer_nums: List[int],
                 output_num: int,
                 hidden_activation: str = 'relu',
                 output_activation: str = 'sigmoid',
                 seed: Optional[int] = None):
        self.input_num = input_num
        self.hidden_layer_nums = hidden_layer_nums
        self.output_num = output_num
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation
        self.rand = np.random.RandomState(seed)

        self._init_random_weights()
        self._assign_activation_funcs()

    def _init_random_weights(self):
        self.w_matrices = []
        self.b_coefs = []

        layers = [self.input_num]
        layers.extend(self.hidden_layer_nums)
        layers.append(self.output_num)

        for i in range(1, len(layers)):
            self.w_matrices.append(np.random.uniform(-1, 1, size=(layers[i-1], layers[i])))
            self.b_coefs.append(np.random.uniform(-1, 1, size=layers[i]))

    def _assign_activation_funcs(self):
        func_map = {'relu': lambda v: np.maximum(0, v),
                    'sigmoid': lambda v: 1.0 / (1.0 + np.exp(-v))}
        self.hidden_activation = func_map[self.hidden_activation]
        self.output_activation = func_map[self.output_activation]

    def feed_forward(self, X: np.ndarray) -> np.ndarray:
        a = X
        for ind, (w, b) in enumerate(zip(self.w_matrices, self.b_coefs)):
            z = np.dot(a, w) + b
            a = (self.hidden_activation(z)
                 if ind < len(self.w_matrices) - 1
                 else self.output_activation(z))

        return a
