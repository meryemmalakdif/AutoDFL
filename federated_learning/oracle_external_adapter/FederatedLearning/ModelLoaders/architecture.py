import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import ast
class LeNet5(nn.Module):
    def __init__(self):
        super(LeNet5, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5, padding=2) 
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)  # 10 classes for MNIST digits

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), 2)
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def __get_layer_info(self, model):
        layers = []
        total = 0
        for param in model.parameters():
            shape = param.data.shape
            weights = np.prod(shape)
            total += weights
            layers.append((shape, weights))
        return layers, total

    def set_weights(self ,model, flattened_weights):
    #     with open('mimi.txt', 'a') as f:
    #   # Write the submissions_evaluation to the file
    #         f.write(f"hihi  : {flattened_weights}\n") 
    #     flattened_weights = ast.literal_eval(flattened_weights.decode())
        index = 0
        for param in model.parameters():
            param_shape = param.data.shape
            param_length = param.data.numel()
            
            # Convert numpy array to Python list and then create a tensor
            new_param_data = torch.tensor(flattened_weights[index:index+param_length].tolist()).view(param_shape)
            param.data = new_param_data
            index += param_length

    # def set_weights(self, model, flattened_weights):
    #     index = 0
    #     for param in model.parameters():
    #         param_shape = param.data.shape
    #         param_length = param.data.numel()
            
    #         # Convert the bytes object to a list of floats
    #         flattened_weights_list = [float(x) for x in flattened_weights.decode().split(',')]
            
    #         # Create a PyTorch tensor from the list of weights
    #         new_param_data = torch.tensor(flattened_weights_list[index:index+param_length]).view(param_shape)
    #         param.data = new_param_data
    #         index += param_length



# Instantiate the model
model = LeNet5()

