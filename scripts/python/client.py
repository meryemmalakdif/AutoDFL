import click
import torch.nn as nn
import torch.optim as optim
import os
import time
from FederatedLearning import trainer
from FederatedLearning import task_requester
from FederatedLearning import smart_contract_functions
from FederatedLearning import utilities
from FederatedLearning import ModelLoaders
from FederatedLearning import weights_loaders
from FederatedLearning.utilities import load_data




@click.command()
@click.option('--provider', default='http://127.0.0.1:3050', help='web3 API HTTP provider to layer 2')
@click.option('--abi', default='./build/contracts/NoScore.json', help='contract abi file')
@click.option('--ipfs', default='/ip4/127.0.0.1/tcp/5001', help='IPFS api provider')
@click.option('--account', help='account address', required=True)
@click.option('--passphrase', help='zksync layer private key', required=True)
@click.option('--contract', help='contract address', required=True)
@click.option('--train', required=True)
@click.option('--test', required=True)
@click.option('--learning_rate', required=True)
@click.option('--epochs', required=True)
@click.option('--task', required=True)
def main(provider, abi, ipfs, account, passphrase, contract, train, test, learning_rate, epochs, task):
  # Get Contract
  contract_task = smart_contract_functions.Contract_zksync(provider, abi, contract, passphrase) 
  # we re doing this because when we pass args from bash script , the scripts gets them as a string for some reason  yaelmha rabi
  if not isinstance(task, int):
    try:
      task = int(task)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid task id provided")
  if not isinstance(learning_rate, float):
    try:
      learning_rate = float(learning_rate)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid learning rate provided")
                    
  if not isinstance(epochs, int):
    try:
      epochs = int(epochs)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid epochs number provided")
  weights_loader = weights_loaders.IpfsWeightsLoader(ipfs)
  model_loader = ModelLoaders.IpfsModelLoader(contract, weights_loader, ipfs_api=ipfs)
  contract_task.register_as_trainer()  

  # register to the task
  tx, tx_receipt = contract_task.register_as_trainer_task(task)
  # wait some time before checking if the task's current phase is training
  while True:
    # get the task details to access the model cid
    time.sleep(5)
    current_task = contract_task.get_task_byId(task)
    if current_task[10] == "training":
      break
  chosen_trainers = contract_task.get_trainers_task(task)
  status = contract_task.is_element_in_array(chosen_trainers,account)
  if status:
    i=0
    while True:
      if i==0:
        model = model_loader.load(current_task[1]) 
      else:
        model = model_loader.load(current_task[1],current_task[5]) 
      # load train and test data
      train_loader = load_data(train)
      test_loader = load_data(test)
      criterion = nn.CrossEntropyLoss()
      optimizer = optim.SGD(model.parameters(), lr=learning_rate)
      model_trainer = trainer.Trainer(model,task,contract,account,ipfs)

      result = model_trainer.train(model, criterion, optimizer , train_loader, test_loader , epochs)
      # Accessing the weights of the trained model
      weights = model_trainer.get_weights(model)
      weights_path = model_trainer.store(weights)
      model_weights_ipfs_hash = model_trainer.store_weights_ipfs(weights_path)
      trainingAccuracy = utilities.float_to_int(result['train_acc'])
      update = {
        "trainingAccuracy": trainingAccuracy,
        "trainingDataPoints": len(train_loader.dataset),
        "weights": model_weights_ipfs_hash
        }

      transaction, transaction_receipt = contract_task.upload_model(update,task,i)
      i+=1 
      if i!=current_task[7] :
        time.sleep(10)
        while True:
          # get the task details to access its state
          current_task = contract_task.get_task_byId(task)
          if current_task[10] == "training":
            break
      else:
        break
      time.sleep(0.5)
  else:
    print("trainer is not selected for the task ")

main()  