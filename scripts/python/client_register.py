import click
from FederatedLearning import smart_contract_functions



@click.command()
@click.option('--provider', default='http://127.0.0.1:3050', help='web3 API HTTP provider to layer 2')
@click.option('--abi', default='./build/contracts/NoScore.json', help='contract abi file')
@click.option('--account', help='account address', required=True)
@click.option('--passphrase', help='zksync layer private key', required=True)
@click.option('--contract', help='contract address', required=True)
def main(provider, abi, account, passphrase, contract):
  # Get Contract
  contract_task = smart_contract_functions.Contract_zksync(provider, abi, contract, passphrase) 
  # register to the BFL system
  contract_task.register_as_trainer()
 
main()  