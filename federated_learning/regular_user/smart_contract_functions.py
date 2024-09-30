import json
from pathlib import Path
from enum import Enum
from web3 import Web3
from web3.middleware import geth_poa_middleware
import warnings
import binascii
import time
from web3.gas_strategies.time_based import medium_gas_price_strategy
warnings.filterwarnings("ignore", category=UserWarning, module='web3')

def is_valid_private_key(private_key):
    try:
        # Remove the "0x" prefix if present
        if private_key.startswith("0x"):
            private_key = private_key[2:]

        # Check if the private key is a valid hexadecimal string
        binascii.unhexlify(private_key)

        # Check if the private key length is exactly 32 bytes (64 characters)
        if len(private_key) != 64:
            return False

        return True
    except (ValueError, TypeError):
        return False
    
def get_web3_l1(provider, abi_file, account, passphrase, contract_address):

  # provider url specifying the Ethereum node provider
  # abi_file: A file containing the ABI (Application Binary Interface) of the smart contract.
  # account: The Ethereum account used for interacting with the contract , sending transactions ...
  # passphrase: The password for unlocking the Ethereum account
  # contract: The address of the deployed smart contract 

  ## Provider Initializer
  provider = Web3.HTTPProvider(provider)
  abi = get_abi(abi_file)
  account = Web3.to_checksum_address(account)

  ## the main interface for interacting with the Ethereum network
  web3 = Web3(provider)
  # injects middleware into the Web3 instance to handle Proof of Authority (PoA) consensus algorithms
  web3.middleware_onion.inject(geth_poa_middleware, layer=0)
  # unlocks the specified Ethereum account for 600 seconds (10 minutes) using the provided passphrase
  print("address ",account)
  print("password ",passphrase)
  web3.geth.personal.unlock_account(account, passphrase, 600)

  contract = web3.eth.contract(address=contract_address, abi=abi)
  defaultOpts = { 'from': account,
                         # Define gas price and gas limit
                  "gas_price" : web3.to_wei('20', 'gwei'),  # Example: 20 gwei
                  "gas_limit" : 200000  # Set an appropriate gas limit based on your 
                 
                  }


  return (web3, contract, defaultOpts, abi)



# setting up a connection to a Ethereum network and interacting with a smart contract deployed on that network
def get_web3(provider, abi_file, contract_address):
  # provider url specifying the Ethereum node provider
  # abi_file: A file containing the ABI (Application Binary Interface) of the smart contract.
  # account: The Ethereum account used for interacting with the contract , sending transactions ...
  # passphrase: The password for unlocking the Ethereum account
  # contract: The address of the deployed smart contract 

  ## Provider Initializer
  provider = Web3.HTTPProvider(provider)
  abi = get_abi(abi_file)
  ## the main interface for interacting with the Ethereum network
  web3 = Web3(provider)
  # injects middleware into the Web3 instance to handle Proof of Authority (PoA) consensus algorithms
  web3.middleware_onion.inject(geth_poa_middleware, layer=0)
  web3.eth.set_gas_price_strategy(medium_gas_price_strategy)
  # unlocks the specified Ethereum account for 600 seconds (10 minutes) using the provided passphrase
  # using the passphrase
  # web3.geth.personal.unlock_account(account, passphrase, 600)
  print("c du rai ",contract_address)
  contract = web3.eth.contract(address=contract_address, abi=abi)
  #defaultOpts = { 'from': account.address }

  return (web3, contract, abi)


# setting up a connection to the zksync rollup and interacting with a smart contract deployed on it
def get_contract_from_zksync(provider, abi_file, contract_address):
  # fetch abi array from the abi json file
  abi = get_abi(abi_file)
  # Connect to zkSync testnet
  zksync_provider = Web3(Web3.HTTPProvider(provider))
  zksync_provider.middleware_onion.inject(geth_poa_middleware, layer=0)
  # Create a contract instance
  contract = zksync_provider.eth.contract(address=contract_address, abi=abi)
  return (zksync_provider, contract , abi)



def get_abi(filename):
  with open(filename) as file:
    contract_json = json.load(file)
  return contract_json['abi']


class RoundPhase(Enum):
  STOPPED = 0
  WAITING_FOR_UPDATES = 1
  WAITING_FOR_SCORES = 2
  WAITING_FOR_AGGREGATIONS = 3
  WAITING_FOR_TERMINATION = 4


class ContractLayer1():
  def __init__(self, provider, abi_file, account, passphrase, contract_address):
    self.account = account
    # password or passphrase for unlocking the Ethereum account associated with the contract
    self.passphrase = passphrase
    (web3, contract, default_opts, abi) = get_web3_l1(provider, abi_file, account, passphrase, contract_address)
    self.web3 = web3
    self.contract = contract
    self.abi = abi
    self.default_opts = default_opts
  def get_all_tasks(self):
    return self.contract.functions.getAllTasks().call(self.default_opts)


  def publish_task(self, modelCid, infoCid,roundsNumber,trainersNumber):
    self.unlock_account()
    transaction = self.contract.functions.publishTask(modelCid, infoCid, roundsNumber,trainersNumber).transact(self.default_opts)
    return transaction, self.__wait_tx(transaction)
  def __wait_tx(self, tx):
      try:
          # receipt provides information about the outcome of a transaction
          receipt = self.web3.eth.wait_for_transaction_receipt(tx)
          return receipt
      except Exception as e:
          # Handle the exception here
          print(f"Error waiting for transaction receipt: {e}")
          # You can also raise a custom exception or return a default value
          raise Exception("Failed to get transaction receipt")



  def unlock_account(self):
    self.account = Web3.to_checksum_address(self.account)
    
    self.web3.geth.personal.unlock_account(self.account, self.passphrase, 600)

class Contract():
  def __init__(self, provider, abi_file, contract_address, private_key):
    # password or passphrase for unlocking the Ethereum account associated with the contract
    self.private_key = private_key
    (web3, contract, abi) = get_web3(provider, abi_file, contract_address)
    self.web3 = web3
    self.contract = contract
    self.abi = abi

  def get_all_tasks(self):
    return self.contract.functions.getAllTasks().call()

  def publish_task(self, modelCid, infoCid,roundsNumber,trainersNumber):
    # Load your private key
    print(self.private_key)
    account = self.web3.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.publishTask(modelCid, infoCid, roundsNumber,trainersNumber).build_transaction({
        'from': account.address,
        'nonce': self.web3.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)



  async def handle_event(event):
    print("event printed ",event)
  '''
  here basically we can call all the functions that we ve defined in the smart contracts
  self.contract.functions.function_name().call(self.default_opts) => doesn t modify BC state
  self.contract.functions.function_name().transact(self.default_opts) => changes BC state
  '''
  
  def evaluation_admin(self, local_hash, trainers, model_hash, global_weights_hash,  evaluation, round):
    # Load your private key
    account = self.web3.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.requestVolumeData(local_hash, trainers, model_hash, global_weights_hash,  evaluation , round).build_transaction({
        'from': account.address,
        'nonce': self.web3.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)

  def pre_rep(self, addr, values):
    # Load your private key
    account = self.web3.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.requestPreRepData(addr, values).build_transaction({
        'from': account.address,
        'nonce': self.web3.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
  

  def trigger_aggregation_admin(self, local_models, scores, model_hash):
    # Load your private key
    account = self.web3.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.requestAggregation(local_models, scores, model_hash).build_transaction({
        'from': account.address,
        'nonce': self.web3.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
  

  def scores_admin(self):
    return self.contract.functions.getVolume().call()

  def pre_rep_result(self):
    return self.contract.functions.getPreRep().call()
  
  def pre_rep_result_trainers(self):
    return self.contract.functions.getTrainers().call()



  def behaviour_trainers(self):
    return self.contract.functions.getBehaviour().call()
    
  def get_global_model_weights_hash(self):
    return self.contract.functions.getGlobalModelWeightsHash().call()
  
  def authorize(self, senders):
    # Load your private key
    account = self.web3.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setAuthorizedSenders(senders).build_transaction({
        'from': account.address,
        'nonce': self.web3.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)


  # This function essentially provides logging for the start and end of a transaction,
  # along with relevant details such as the transaction hash, gas used, and timestamps.
  # It's useful for tracking and monitoring transaction execution in a Python application
  # interacting with Ethereum through the web3.py library

  def unlock_account(self):
    self.web3.geth.personal.unlock_account(self.account, self.passphrase, 600)
  
  def wait_tx(self, tx , private_key):
    if not isinstance(private_key, str):
      try:
          private_key = str(private_key)
      except ValueError:
          # Handle invalid input gracefully (e.g., raise custom exception or use a default)
          raise ValueError("Invalid private key id provided")
    print("admin private key ",private_key)
    signed_tx = self.web3.eth.account.sign_transaction(tx,private_key)
    tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt

class Contract_zksync():
  def __init__(self, provider, abi_file, contract_address, private_key):

    ( zksync_provider , contract , abi )= get_contract_from_zksync(provider, abi_file, contract_address)
    self.contract = contract
    self.zksync_provider = zksync_provider
    self.private_key = private_key
    self.contract_address = contract_address
    self.abi = abi


  def publish_task(self, modelCid, infoCid,roundsNumber,trainersNumber):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.publishTask(modelCid, infoCid, roundsNumber,trainersNumber).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)

  def update_global_model_weights(self ,taskId , globalModel , state):
      # Load your private key
      account = self.zksync_provider.eth.account.from_key(self.private_key)
      # Build and send the transaction
      tx = self.contract.functions.UpdateGlobalModelWeights(taskId,globalModel,state).build_transaction({
          'from': account.address,
          'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
      })
      return tx , self.wait_tx(tx,self.private_key)
  
  def update_task_state(self ,taskId , state):
      # Load your private key
      account = self.zksync_provider.eth.account.from_key(self.private_key)
      # Build and send the transaction
      tx = self.contract.functions.updateTaskState(taskId,state).build_transaction({
          'from': account.address,
          'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
      })
      return tx , self.wait_tx(tx,self.private_key)
  
  
  def register_as_trainer(self):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    checksum_address = self.zksync_provider.to_checksum_address(account.address)
    # Build and send the transaction
    tx = self.contract.functions.registerTrainer().build_transaction({
        'from': checksum_address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
   
  def register_as_trainer_task(self,taskId):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    checksum_address = self.zksync_provider.to_checksum_address(account.address)
    # Build and send the transaction
    tx = self.contract.functions.registerTrainerTask(taskId).build_transaction({
        'from': checksum_address,
        'nonce': self.zksync_provider.eth.get_transaction_count(checksum_address)+1
    })
    return tx , self.wait_tx(tx,self.private_key)

  def scores_admin(self):
    return self.contract.functions.getVolume().call()


  def behaviour_trainers(self):
    return self.contract.functions.getBehaviour().call()
    
  
  def set_task_trainers(self,taskId,trainers):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setTaskTrainers(taskId,trainers).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
    
  def set_task_trainers_round(self,taskId,round,trainers):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setTaskRoundTrainers(taskId,round,trainers).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)

  def testit(self,taskId,round,trainers):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.testit(taskId,round,trainers).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
          



  def is_trainer_for_task(self,taskId,address):
    return self.contract.functions.isTrainerForTask(taskId,address).call()

  def get_trainers_task(self,taskId):
    return self.contract.functions.getTrainersForTask(taskId).call()
    

  def is_element_in_array(self,array,address):
    return self.contract.functions.isInAddressArray(array,address).call() 
    
  def get_updates_task(self,task,round):
    return self.contract.functions.getUpdatesForAggregationTask(task,round).call()
   



  def requestVolume(self, local_hash, model_hash, global_weights_hash,  evaluation, round):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.requestVolumeData(local_hash, model_hash, global_weights_hash,  evaluation , round).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)


  
  def evaluation_admin(self, local_hash, trainers, model_hash, global_weights_hash,  evaluation, round):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.requestVolumeData(local_hash, trainers, model_hash, global_weights_hash,  evaluation , round).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)


  def triggerEvaluation(self, task, round, evaluation):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.triggerEvaluation( task, round, evaluation ).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)+1
    })
    return tx , self.wait_tx(tx,self.private_key)

   



  def get_trainers_task_round(self,task,round):
    return self.contract.functions.getTrainersForTaskRound(task,round).call()
  
  def get_total_participation_level(self,addr):
    return self.contract.functions.totalParticipationLevel(addr).call()
             
  def gettestit(self,taskId, taskTrainers):
    return self.contract.functions.gettestit(taskId,taskTrainers).call()
  def upload_scores(self, task, round, scores):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.submitScore(task,round,scores).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
  

  def upload_model(self,modelUpdate,task,task_trainers,round):   
      # Encode the update data according to your contract's ABI
      # Encode the struct parameters
      # print(self.web3.eth)
      # encoded_data =  self.web3.eth.abi.encode_abi(
      #   ["uint", "uint", "uint", "string"],
      #   [modelUpdate["trainingAccuracy"], modelUpdate["testingAccuracy"], modelUpdate["trainingDataPoints"], modelUpdate["weights"]]
      #   )   
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    checksum_address = self.zksync_provider.to_checksum_address(account.address)
    # Build and send the transaction
    tx = self.contract.functions.submitUpdate(modelUpdate,task,task_trainers,round).build_transaction({
        'from': checksum_address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
      
  def get_round(self):
    return self.contract.functions.round().call()

  def get_round_phase(self):
    return RoundPhase(self.contract.functions.roundPhase().call())

  def get_training_round(self):
    [round, weights_cid] = self.contract.functions.getRoundForTraining().call()
    return (round, weights_cid)
  

  def get_all_tasks(self):
    return self.contract.functions.getAllTasks().call()

  def get_task_byId(self, id):
    return self.contract.functions.getTaskById(id).call()
  
  def start_round(self, *args):
    self.unlock_account()
    tx = self.contract.functions.startRound(*args).transact()
    return tx, self.__wait_tx(tx)
  
  def get_trainers(self):
    return self.contract.functions.getTrainers().call()
  





  # def get_submissions_for_aggregation(self):
  #   [round, trainers, submissions] = self.contract.functions.getUpdatesForAggregation().call(self.default_opts)
  #   return (round, trainers, submissions)
  def submit_aggregation(self, weights_id,task,task_aggregators,round):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.submitAggregation(weights_id,task,task_aggregators,round).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)
  

  def setPosNeg(self, taskId,addr,round):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setPosNeg(taskId,addr,round).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)

  def deposit(self, amount):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.deposit().build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address),
        'value': amount
    })
    return tx , self.wait_tx(tx,self.private_key)

  def withdraw(self, amount, receipient):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.withdraw(amount, receipient).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)


  def get_balance(self,addr):
    return self.contract.functions.getBalance(addr).call()
  
  def get_state_task_round(self,task):
    return self.contract.functions.getTaskState(task).call()
    
  def get_number(self):
    return self.contract.functions.getNUmber().call()
    
  def get_updates_task_round(self,task,round):
    return self.contract.functions.updatesTask(task,round).call()
  
  def get_scores_task_round(self,task,round):
    return self.contract.functions.getRoundScores(task,round).call()
  
  def get_single_update(self,task,task_trainer,round):
    return self.contract.functions.getSingleUpdate(task,task_trainer,round).call()

  def get_aggregations_task_round(self,task,round):
    return self.contract.functions.aggregationsTask(task,round).call()
  
  def get_all_reputation(self):
    return self.contract.functions.getAllReputations().call()

  def getPosNeg(self,taskId,addr,round):
    return self.contract.functions.getPosNeg(taskId,addr,round).call()
  

  def get_eh(self,_taskPublisher,_trainer):
    return self.contract.functions.ehPositive(_taskPublisher,_trainer).call()
  

  def get_greeting(self): 
    return self.contract.functions.testConcatenate().call()
  

  
  
  def set_greeting(self):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setGreeting('Hello, zkSync!').build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)

  def measureTrainersPerformance(self, task, startingRound, finishingRound, trainer, method):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.measurePerformance(task, startingRound, finishingRound, trainer, method).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)    
    
  
  def detect_interaction(self, score , scores, method):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.detect_interaction(score , scores , method).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)    
     

  def update_reputation(self, taskId, startingRound , finishingRound, addrs ,  scores , completeness):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.updateRepuation(taskId,startingRound,finishingRound,addrs , scores , completeness).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)+1
    })
    return tx , self.wait_tx(tx,self.private_key)    
     
  def hihi(self, taskId, startingRound , finishingRound, addr , method ):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.hihi(taskId,startingRound,finishingRound,addr,method).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)+1
    })
    return tx , self.wait_tx(tx,self.private_key)    
     


  
  def set_business_logic(self, addr):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setBusinessContract(addr).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)



  def authorize(self, senders):
    # Load your private key
    account = self.zksync_provider.eth.account.from_key(self.private_key)
    # Build and send the transaction
    tx = self.contract.functions.setAuthorizedSenders(senders).build_transaction({
        'from': account.address,
        'nonce': self.zksync_provider.eth.get_transaction_count(account.address)
    })
    return tx , self.wait_tx(tx,self.private_key)








  def wait_tx(self, tx , private_key):
    start_time = time.time()
    timeout = 120
    poll_interval=5
    if not isinstance(private_key, str):
      try:
          private_key = str(private_key)
      except ValueError:
          # Handle invalid input gracefully (e.g., raise custom exception or use a default)
          raise ValueError("Invalid private key id provided")
    signed_tx = self.zksync_provider.eth.account.sign_transaction(tx,private_key)
    tx_hash = self.zksync_provider.eth.send_raw_transaction(signed_tx.rawTransaction)
    while True:
        try:
            tx_receipt = self.zksync_provider.eth.wait_for_transaction_receipt(tx_hash, timeout=poll_interval)
            break
        except Exception as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Transaction {tx_hash.hex()} timed out after {timeout} seconds")
            else:
                print(f"Waiting for transaction {tx_hash.hex()} to be mined...")
                time.sleep(poll_interval)
    #tx_receipt = self.zksync_provider.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt



