
import click
# Get the path to the FederatedLearning directory relative to my_script.py
from FederatedLearning import task_requester
from FederatedLearning import smart_contract_functions
from FederatedLearning import ModelLoaders
from pathlib import Path



@click.command()
@click.option('--provider', default='http://127.0.0.1:8545', help='web3 API HTTP provider')
@click.option('--abi', default='./build/contracts/NoScore.json', help='contract abi file')
@click.option('--ipfs', default='/ip4/127.0.0.1/tcp/5001', help='IPFS api provider')
@click.option('--account', help='account address')
@click.option('--passphrase', help='account private key')
@click.option('--contract', help='contract address', required=True)
@click.option('--rounds', help='rounds number', required=True)
@click.option('--required_trainers_number', help='trainers number', required=True)
def main(provider, abi , ipfs, account, passphrase, contract, rounds, required_trainers_number):
  contract_task = smart_contract_functions.Contract_zksync(provider, abi, contract, passphrase) 
  if not isinstance(rounds, int):
    try:
      rounds = int(rounds)
    except ValueError:
      # Handle invalid input gracefully (e.g., raise custom exception or use a default)
      raise ValueError("Invalid rounds number id provided")  
  if not isinstance(required_trainers_number, int):
    try:
        required_trainers_number = int(required_trainers_number)
    except ValueError:
        # Handle invalid input gracefully (e.g., raise custom exception or use a default)
        raise ValueError("Invalid required trainers number")
  # instanciate model class
  model = ModelLoaders.LeNet5()
  model_info = "A model to classify digits from 0 to 9"
  task_publisher = task_requester.TaskRequester(ipfs)
  model_path, info_path = task_publisher.serialize_and_save_model(model,model_info)
  model_ipfs_hash, info_ipfs_hash = task_publisher.store_model(model_path,info_path)
  transaction, transaction_receipt = contract_task.publish_task(model_ipfs_hash, info_ipfs_hash,rounds,required_trainers_number)
  print("The current task id is",len(contract_task.get_all_tasks()))

main()