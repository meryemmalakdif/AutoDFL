import torch
import torch.nn as nn
import numpy as np

class Model:
    def __init__(self, model):
        self.model = model
        self.layers, self.count = self.__get_layer_info(model)

    def __get_layer_info(self, model):
        layers = []
        total = 0
        for param in model.parameters():
            shape = param.data.shape
            weights = np.prod(shape)
            total += weights
            layers.append((shape, weights))
        return layers, total


    def evaluate(self, x_val, y_val):
        # Implement your evaluation logic here using PyTorch evaluation procedures
        return {}  # Return evaluation metrics

    def get_weights(self):
        weights = []
        for param in self.model.parameters():
            weights.extend(param.data.cpu().numpy().flatten().tolist())
        return np.array(weights)

    def set_weights(self, serialized):
        if len(serialized) != self.count:
            raise Exception(f'Wrong number of serialized weights. Expected {self.count}, got {len(serialized)}')

        i = 0
        for param in self.model.parameters():
            shape = param.data.shape
            count = np.prod(shape)
            w = serialized[i:i+count]
            i += count
            w = np.array(w).reshape(shape)
            param.data.copy_(torch.from_numpy(w))

# Usage example:
# Instantiate your PyTorch model and then create an instance of the Model class with your model.
# pytorch_model = YourPyTorchModel()
# model_wrapper = Model(pytorch_model)
