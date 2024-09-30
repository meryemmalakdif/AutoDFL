import numpy as np
import json
import torch
import torch.optim as optim
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import functional as F

from torch.autograd import Variable
import torch.utils.data as data
from torch.utils.data import TensorDataset, DataLoader
import argparse
import logging
import os
import copy
from math import *
import random

import datetime
#from torch.utils.tensorboard import SummaryWriter
from datasets import MNIST_truncated
from utils import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='mnist', help='dataset used for training')
    parser.add_argument('--partition', type=str, default='homo', help='the data partitioning strategy')
    parser.add_argument('--n_parties', type=int, default=2,  help='number of workers in a distributed cluster')
    parser.add_argument('--init_seed', type=int, default=0, help="Random seed")
    parser.add_argument('--datadir', type=str, required=False, default="./data/", help="Data directory")
    parser.add_argument('--logdir', type=str, required=False, default="./logs/", help='Log directory path')
    parser.add_argument('--beta', type=float, default=0.5, help='The parameter for the dirichlet distribution for data partitioning')
    parser.add_argument('--device', type=str, default='cuda:0', help='The device to run the program')
    parser.add_argument('--log_file_name', type=str, default=None, help='The log file name')
    args = parser.parse_args()
    return args




def get_partition_dict(dataset, partition, n_parties, init_seed=0, datadir='./data', logdir='./logs', beta=0.5):
    seed = init_seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)
    #X_train, y_train, X_test, y_test, net_dataidx_map, traindata_cls_counts = partition_data(
    #    dataset, datadir, logdir, partition, n_parties, beta=beta)

    #return net_dataidx_map

def split_data_save_file(dataset, partition, n_parties, init_seed=0, datadir='./data', logdir='./logs', beta=0.5):
    seed = init_seed
    np.random.seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)
    X_train, y_train, X_test, y_test, net_dataidx_map, net_dataidx_map_test, traindata_cls_counts, traindata_cls_counts_test = partition_data(
        dataset, datadir, logdir, partition, n_parties, beta=beta)
    
    #transform = transforms.Compose([transforms.ToTensor()])
    # for Mnist dataset we add greyscale because they have a single channel instead of 3
    # transform = transforms.Compose([
    # transforms.Grayscale(),  # Convert to grayscale if needed
    # transforms.ToTensor()
    # ])

    # Load and transform the MNIST dataset
    transform = transforms.Compose([
        transforms.Resize((32, 32)),  # Resize images to 32x32
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))  # Normalize using mean and std of MNIST
    ])

    # Assuming you have mnist_dataobj created earlier
    mnist_train_ds = MNIST_truncated(datadir, train=True, download=True, transform=transform)
    mnist_test_ds = MNIST_truncated(datadir, train=False, download=True, transform=transform)

    images , labels = mnist_train_ds.data, mnist_train_ds.target
    images_test , labels_test = mnist_test_ds.data, mnist_test_ds.target

    party_data_map = {}  # Create a dictionary to store party-specific data
    for party_id, indices in net_dataidx_map.items():
        party_data_map[party_id] = {
            'images': [images[i] for i in indices],  # Include both images and labels
            'labels': [labels[i] for i in indices]
        }   

    party_data_map_test = {}
    for party_id, indices in net_dataidx_map_test.items():
        party_data_map_test[party_id] = {
            'images': [images_test[i] for i in indices],  # Include both images and labels
            'labels': [labels_test[i] for i in indices]
        }  

  # Create the directory if it doesn't exist
    os.makedirs(datadir+"/train", exist_ok=True)
    os.makedirs(datadir+"/test", exist_ok=True)

    for party_id, data in party_data_map.items():
      filename = os.path.join(datadir+"/train", f"party_{party_id}.npz")
      np.savez_compressed(filename, images=data['images'], labels=data['labels'])

    for party_id, data in party_data_map_test.items():
      filename = os.path.join(datadir+"/test", f"party_{party_id}.npz")
      np.savez_compressed(filename, images=data['images'], labels=data['labels'])


# for testing purposes
def train_model(data_path, model_class, learning_rate=0.01, epochs=100):
  """
  Trains a model using data from a `.npz` file.

  Args:
      data_path: Path to the `.npz` file containing images and labels.
      model_class: The PyTorch model class to use.
      learning_rate: Learning rate for the optimizer (default: 0.01).
      epochs: Number of training epochs (default: 10).

  Returns:
      The trained model.
  """

  # Load data from the `.npz` file
  data = np.load(data_path)
  images, labels = data['images'], data['labels']

  # Convert data to PyTorch tensors
  images = torch.from_numpy(images).float()
  labels = torch.from_numpy(labels).long()

  # Reshape images to expected format (batch_size, 784)
  images = images.view(-1, 28 * 28)  # Assuming all images have the same size


  # Create a dataset and data loader
  dataset = TensorDataset(images, labels)
  data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

  # Instantiate the model
  model = model_class()

  # Define loss function and optimizer
  criterion = nn.CrossEntropyLoss()
  optimizer = optim.SGD(model.parameters(), lr=learning_rate)

  # Train the model
  for epoch in range(epochs):
      for i, (images, labels) in enumerate(data_loader):
          # Forward pass
          outputs = model(images)
          loss = criterion(outputs, labels)

          # Backward pass and update weights
          optimizer.zero_grad()
          loss.backward()
          optimizer.step()

          if (i + 1) % 100 == 0:
              print(f"Epoch [{epoch+1}/{epochs}], Step [{i+1}/{len(data_loader)}], Loss: {loss.item():.4f}")

  return model

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        x = self.linear(x)
        return x



if __name__ == '__main__':
    # torch.set_printoptions(profile="full")
    args = get_args()
    mkdirs(args.logdir)
    if args.log_file_name is None:
        argument_path='experiment_arguments-%s.json' % datetime.datetime.now().strftime("%Y-%m-%d-%H:%M-%S")
    else:
        argument_path=args.log_file_name+'.json'
    with open(os.path.join(args.logdir, argument_path), 'w') as f:
        json.dump(str(args), f)
    device = torch.device(args.device)
    # logging.basicConfig(filename='test.log', level=logger.info, filemode='w')
    # logging.info("test")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if args.log_file_name is None:
        args.log_file_name = 'experiment_log-%s' % (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M-%S"))
    log_path=args.log_file_name+'.log'
    logging.basicConfig(
        filename=os.path.join(args.logdir, log_path),
        # filename='/home/qinbin/test.log',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M', level=logging.DEBUG, filemode='w')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.info(device)

    seed = args.init_seed
    logger.info("#" * 100)
    np.random.seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)
    logger.info("Partitioning data")
    
    split_data_save_file(dataset=args.dataset, partition=args.partition, n_parties=args.n_parties, datadir=args.datadir, beta=args.beta)

    #model = train_model("./data/train/party_0.npz", MyModel)
    

