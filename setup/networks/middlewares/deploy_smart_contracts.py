import click
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from utils import *

@click.command()
@click.option('-d', '--data-dir', default="./../blockchain/datadir", help='blockchain data directory path')
@click.option('-p', '--provider', default='http://127.0.0.1:8545', help='ethereum API provider')
def deploy_smart_contract(data_dir, provider):
  print(data_dir)
  accounts = read_json(os.path.join(data_dir, 'accounts.json'))
  account_address = list(accounts['owner'].keys())[0]
  account_password = accounts['owner'][account_address]

  ##  Web3 is a Python library for interacting with Ethereum-like blockchains
  web3 = Web3(Web3.HTTPProvider(provider))
  ## to fix that error related to poa chain extraData being 97 instead of 32 or smthg like this 
  #web3.middleware_onion.inject(geth_poa_middleware, layer=0)
  ## It converts the account address to a checksum address 
  ## Checksum addresses are a type of Ethereum address with built-in error checking, ensuring that addresses are entered correctly  
  address = Web3.to_checksum_address(account_address)

  ## takes the account address, password, and a duration (in seconds) for which the account should remain unlocked to sign transactions

  print(address, " ",account_password)
  web3.geth.personal.unlock_account(address, account_password, 1200)
  print("meryeeeeem")

  os.system("cd ../.. && truffle migrate --reset")
  #os.system("cd ../.. && truffle migrate --network development") # same error 
  print("meryeeeeem")


deploy_smart_contract()