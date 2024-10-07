import click
import os
import time

# Get the path to the FederatedLearning directory relative to my_script.py
from FederatedLearning import smart_contract_functions
from FederatedLearning import task_requester




current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")




@click.command()
@click.option('--provider', default='http://127.0.0.1:3050', help='web3 API HTTP provider for layer 2')
@click.option('--provider_layer1', default='http://127.0.0.1:8545', help='web3 API HTTP provider for layer 1')
@click.option('--abi', default='', help='contract abi file')
@click.option('--abi_oracle', default='', help='oracle contract abi file')
@click.option('--abi_rep', default='', help='reputation contract abi file')
@click.option('--ipfs', default='/ip4/127.0.0.1/tcp/5001', help='IPFS api provider')
@click.option('--account', help='account address needed to interact with the layer 2 and layer 1', required=True)
@click.option('--passphrase', help='private key needed to interact with the layer 2 and layer 1', required=True)
@click.option('--contract', help='task contract address', required=True)
@click.option('--contract_oracle', help='oracle contract address', required=True)
@click.option('--contract_rep', help='reputation contract address', required=True)
@click.option('--task', required=True) 
@click.option('--evaluation', required=True) 
def main(provider, provider_layer1,  abi, abi_oracle, abi_rep, ipfs, account, passphrase, contract, contract_oracle, contract_rep, task, evaluation):
  # we re doing this because when we pass args from bash script , the scripts gets them as a string for some reason  yaelmha rabi
  if not isinstance(passphrase, str):
    try:
      passphrase = str(passphrase)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid private key provided")  
  if not isinstance(evaluation, str):
    try:
      evaluation = str(evaluation)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid evaluation method")  
  if not isinstance(task, int):
    try:
      task = int(task)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid task id provided")
    
  # Get the oracle contract
  contract_layer1 = smart_contract_functions.Contract(provider_layer1, abi_oracle, contract_oracle, passphrase)

  contract_task = smart_contract_functions.Contract_zksync(provider, abi, contract, passphrase)

  # Get access to reputation contract -deployed on layer 2- functions
  contract_reputation = smart_contract_functions.Contract_zksync(provider, abi_rep, contract_rep, passphrase)
  i=0
  time.sleep(10)
  while True:
    current_task = contract_task.get_task_byId(task)
    if len(current_task[9])>0:
      break  

  task_requester_instance = task_requester.TaskRequester(ipfs)
  selected_trainers = task_requester_instance.selectTrainers(current_task[9],current_task[8])  
  time.sleep(10)
  contract_task.set_task_trainers(task,selected_trainers)


  while True:
    # get the task details
    current_task = contract_task.get_task_byId(task)
    if current_task[10] == "evaluation":
      break  

  while True:
    while True:
      local_updates = contract_task.get_updates_task(task,i)
      if len(local_updates)>0:
        break

 

    
    local_hash = "-".join(local_updates)
    trainers = "-".join(current_task[4])

    if current_task[5]:
      global_model_weights = current_task[5]
    else:
      global_model_weights=""





    tx, tx_receipt = contract_layer1.evaluation_admin(local_hash, trainers, current_task[1] , global_model_weights , evaluation, str(i))
    sc = contract_layer1.scores_admin()  

    behaviour = contract_layer1.behaviour_trainers()  

    
    
    while len(sc) == 0:
      sc = contract_layer1.scores_admin() 
      behaviour = contract_layer1.behaviour_trainers()  


  

      
    result = list(zip(current_task[4], sc,behaviour))
    
    contract_task.upload_scores(task,current_task[6],result)
    

    sc = [str(element) for element in sc]
    models_scores = "-".join(sc)


    tx, tx_receipt = contract_layer1.trigger_aggregation_admin(local_hash, models_scores, current_task[1],current_task[5],str(i),trainers)
    global_model_weights_hash = contract_layer1.get_global_model_weights_hash()
    while global_model_weights_hash == "":
      global_model_weights_hash = contract_layer1.get_global_model_weights_hash()
    

    contract_task.update_global_model_weights(task,global_model_weights_hash)

    if (i+1) != current_task[7]:
      i+=1    
      contract_task.update_task_state(task,"training")
      time.sleep(10)
      current_task = contract_task.get_task_byId(task)
  
      while current_task[10]!="evaluation":
        time.sleep(10)
        current_task = contract_task.get_task_byId(task)
    else :  


      my_array = []
      for m in range(0,current_task[7]):
        my_array.append(contract_task.get_scores_task_round(task,m))
 
# we send this to the oracle for pre evaluation 
      addr_list = []
      values_list = []
      data = contract_task.get_scores_task_round(task,i)
      while len(data) == 0: 
        data = contract_task.get_scores_task_round(task,i)
      # Iterate over each tuple in the data
      for entry in data:
        addr_list.append(entry[0])  # Append the address (first element)
        values_list.append(entry[1])  # Append the second element


      addr_list = "-".join(addr_list)
      values_list = '-'.join(map(str, values_list))


      contract_layer1.pre_rep(addr_list, values_list)
      pre_rep = contract_layer1.pre_rep_result() 
      pre_rep_trainers = contract_layer1.pre_rep_result_trainers()  
      while len(pre_rep) == 0:
        pre_rep = contract_layer1.pre_rep_result() 
        pre_rep_trainers = contract_layer1.pre_rep_result_trainers()

      pre_rep_trainers = pre_rep_trainers.split("-")

      counts = [0] * len(pre_rep_trainers)

      # Iterate through each sublist in the data
      for sublist in my_array:
          
        for entry in sublist:
          address = entry[0]  # The address is the first element
          amount = entry[1]   # The second element is the accuracy of a trainer's local model
              
          # Check if the amount is greater than 0 => the trainer did not skip the round
          if amount > 0:
            index = pre_rep_trainers.index(address)     
            counts[index] += 1

      contract_reputation.update_reputation(task,  pre_rep_trainers ,  pre_rep , counts )

      time.sleep(10)


      contract_task.update_task_state(task,"done")
      break






def extract_addresses_and_concatenate(data):
    # Step 1: Extract unique addresses
    unique_addresses = set()
    for sublist in data:
        for item in sublist:
            unique_addresses.add(item[0])
    
    # Step 2: Initialize lists to hold addresses and concatenated second values
    addresses_list = []
    concatenated_values_list = []
    
    # Step 3: Iterate through the data again to concatenate second values for each address
    for address in unique_addresses:
        second_values = []
        for sublist in data:
            for item in sublist:
                if item[0] == address:
                    second_values.append(item[1])
        # Concatenate the second values for this address
        concatenated_values = '-'.join(map(str, second_values))
        
        # Append address and concatenated values to their respective lists
        addresses_list.append(address)
        concatenated_values_list.append(concatenated_values)
    
    return addresses_list, concatenated_values_list



main()  