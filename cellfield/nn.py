from typing import Optional
import numpy as np
from numpy.typing import ArrayLike


class FeedForwardNetwork:
    def __init__(self,
                 input_num: int,
                 hidden_layer_nums: list[int],
                 output_num: int,
                 hidden_activation: str = 'relu',
                 output_activation: str = 'sigmoid',
                 seed: Optional[int] = None,
                 w_matrices: Optional[list[ArrayLike]] = None,
                 b_weights: Optional[list[ArrayLike]] = None):
        assert (w_matrices and b_weights) or (not w_matrices and not b_weights)

        self.input_num = input_num
        self.hidden_layer_nums = hidden_layer_nums
        self.output_num = output_num
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation
        self.random_gen = np.random.default_rng(seed)

        if w_matrices:
            assert self._is_input_matricies_valid(w_matrices, b_weights)
            self.w_matrices = w_matrices
            self.b_weights = b_weights
        else:
            self._init_random_weights()            
        self._assign_activation_funcs()

    def _init_random_weights(self) -> None:
        self.w_matrices = []
        self.b_weights = []

        layers = [self.input_num]
        layers.extend(self.hidden_layer_nums)
        layers.append(self.output_num)

        for i in range(1, len(layers)):
            self.w_matrices.append(self.random_gen.uniform(-1, 1, size=(layers[i-1], layers[i])))
            self.b_weights.append(self.random_gen.uniform(-1, 1, size=layers[i]))

    def _is_input_matricies_valid(self, w_matrices: list[ArrayLike], b_weights: list[ArrayLike]) -> bool:
        # TODO
        pass

    def _assign_activation_funcs(self) -> None:
        func_map = {'relu': lambda v: np.maximum(0, v),
                    'sigmoid': lambda v: 1.0 / (1.0 + np.exp(-v))}
        self.hidden_activation = func_map[self.hidden_activation]
        self.output_activation = func_map[self.output_activation]

    def feed_forward(self, X: np.ndarray) -> np.ndarray:
        a = X
        for ind, (w, b) in enumerate(zip(self.w_matrices, self.b_weights)):
            z = np.dot(a, w) + b
            a = (self.hidden_activation(z)
                 if ind < len(self.w_matrices) - 1
                 else self.output_activation(z))

        return a
