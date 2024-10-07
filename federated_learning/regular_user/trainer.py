import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import tempfile
import json
import time
import numpy as np
import pickle
import idx2numpy
import chardet
from tqdm import tqdm

class Trainer:
    def __init__(self, model, task,contract, address, ipfs_api='/ip4/127.0.0.1/tcp/5001'):
        #self.model = model
        self.currentTask = task
        self.ipfs_api = ipfs_api
        self.contract = contract
        self.address = address
        self.layers, self.count = self.__get_layer_info(model)
        # register to the system
        # self.__register_trainer()
        # register to a task
        #self.__register_trainer_task(self.currentTask)
      
    
    def __get_layer_info(self, model):
        layers = []
        total = 0
        for param in model.parameters():
            shape = param.data.shape
            weights = np.prod(shape)
            total += weights
            layers.append((shape, weights))
        return layers, total

    def train(self, model, criterion, optimizer, train_loader, val_loader, epochs):
      train_losses = []
      val_losses = []
      train_accs = []
      val_accs = []

      for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for inputs, labels in train_loader:
          optimizer.zero_grad()
          outputs = model(inputs)
          loss = criterion(outputs, labels)
          loss.backward()
          optimizer.step()

          running_loss += loss.item()
          _, predicted = torch.max(outputs.data, 1)
          total_train += labels.size(0)
          correct_train += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_loader)
        train_acc = correct_train / total_train

          # Validation
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
          for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()

          val_loss /= len(val_loader)
          val_acc = correct_val / total_val
      print("Training done...")
      return {'train_loss': train_loss, 'val_loss': val_loss, 'train_acc': train_acc, 'val_acc': val_acc}

    def save_weights(self, model, weights_path='model_weights.json'):
      state_dict = model.state_dict()
    # Serialize the state dictionary to JSON
      with open(weights_path, 'w') as f:
        json.dump(state_dict, f)
    
      return weights_path

     
    def store_weights_ipfs(self, weights_path):

      #dagCBOR.util.serialize(file)
      with tempfile.TemporaryDirectory() as tempdir:
        # Copy the model and info files to the temporary directory
        temp_weights_path = os.path.join(tempdir, os.path.basename(weights_path))
        os.system(f'cp {weights_path} {temp_weights_path}')
        # with open(temp_weights_path, 'rb') as f:
        #   serialized_weights = pickle.load(f)
        # Add the model weights file to IPFS
        model_response = os.popen(f'ipfs add --api {self.ipfs_api} -q {temp_weights_path}').read().strip()
        model_weights_ipfs_hash = model_response.split('\n').pop()
        return model_weights_ipfs_hash

    def store(self, weights,file_path="weights.json"):
      # with tempfile.TemporaryDirectory() as tempdir:
      #   weights_path = os.path.join(tempdir, 'weights.idx')
      # idx2numpy.convert_to_file(weights_path, weights)
      # with open(weights_path, 'rb') as file:
      #   contents = file.read()

      try:
        with open(file_path, 'w') as file:
              # Read the contents of the file
          json.dump(weights.tolist(), file)
      except FileNotFoundError:
          # If the file doesn't exist, create it
        with open(file_path, 'wb') as file:
          print(f"File '{file_path}' created.")
      except IOError:
        print(f"Error occurred while accessing the file '{file_path}'.")


      try:
        if os.path.isfile(file_path):
          with open(file_path, 'r') as file:
            data = json.load(file)
        else:
          print(f"Error: File '{file_path}' not found.")
      except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in file '{file_path}'.")
      except IOError:
        print(f"Error: Unable to read file '{file_path}'.")
  
            

      return file_path

    def get_weights(self,model):
      weights = []
      for param in model.parameters():
        weights.extend(param.data.cpu().numpy().flatten().tolist())
      return np.array(weights)   

    def set_weights(self, serialized, model):
      if len(serialized) != self.count:
        raise Exception(f'Wrong number of serialized weights. Expected ${self.count}, got ${len(serialized)}')

      weights = []
      i = 0

      for (shape, count) in self.layers:
        w = serialized[i:i+count]
        i = i + count
        w = np.array(w)
        w = w.reshape(shape)
        weights.append(w)

      model.set_weights(weights) 

    def retrieve_model_from_ipfs(self, model_ipfs_hash):
      with tempfile.TemporaryDirectory() as tempdir:
        # Download the model file from IPFS
        os.system(f'ipfs get --api {self.ipfs_api} {model_ipfs_hash} -o {tempdir}')
        downloaded_model_path = os.path.join(tempdir, model_ipfs_hash)
        # Load the downloaded model file (assuming it's a PyTorch model)

        # weights = idx2numpy.convert_from_file(downloaded_model_path)

           # Read the file content
        with open(downloaded_model_path, 'rb') as f:
          model_content = f.read()
    

        return model_content

    def load(self, id):
      with tempfile.TemporaryDirectory() as tempdir:
        weights_path = os.path.join(tempdir, 'weights.idx')
        os.system(f"ipfs get --api {self.ipfs_api} -o {weights_path} {id}")
        weights = idx2numpy.convert_from_file(weights_path)
        return weights





    def __register_trainer(self):
      self.contract.register_as_trainer()

    def __register_trainer_task(self,taskId):
      task_trainers = self.contract.get_trainers_task(taskId)
      if self.contract.is_element_in_array(task_trainers,self.address) == False:
        self.contract.register_as_trainer_task(taskId)


  

# Usage example:
# Instantiate the Trainer class with your model and data.
# trainer = Trainer(model, train_x, train_y, test_x, test_y)
# history = trainer.train(criterion, optimizer, train_loader, val_loader, epochs)
