import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)  # Input channels = 1, Output channels = 10
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)  # Input channels = 10, Output channels = 20
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)  # 320 = number of neurons to match the output of the last conv layer
        self.fc2 = nn.Linear(50, 10)  # 10 output classes for MNIST digits (0-9)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)
