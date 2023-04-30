from typing import List, Optional
import numpy as np


class FeedForwardNetwork:
    def __init__(self,
                 input_num: int,
                 hidden_layer_nums: List[int],
                 output_num: int,
                 seed: Optional[int] = None):
        self.input_num = input_num
        self.hidden_layer_nums = hidden_layer_nums
        self.output_num = output_num
        self.rand = np.random.RandomState(seed)        
        self._init_random_weights()

    def _init_random_weights(self):
        self.w_matrices = []
        self.b_coefs = []

        layers = [self.input_num]
        layers.extend(self.hidden_layer_nums)
        layers.append(self.output_num)

        for i in range(1, len(layers)):
            self.w_matrices.append(np.random.uniform(-1, 1, size=(layers[i-1], layers[i])))
            self.b_coefs.append(np.random.uniform(-1, 1, size=layers[i]))

    def feed_forward(self, X: np.ndarray) -> np.ndarray:
        pass
