import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

def load_data(data_path):

  # Load data from the `.npz` file
  data = np.load(data_path)
  images, labels = data['images'], data['labels']

  images = images.reshape(-1, 1, 28, 28)

  # Convert data to PyTorch tensors
  images = torch.from_numpy(images).float()
  labels = torch.from_numpy(labels).long()


  # Create a dataset and data loader
  dataset = TensorDataset(images, labels)
  data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

  return data_loader