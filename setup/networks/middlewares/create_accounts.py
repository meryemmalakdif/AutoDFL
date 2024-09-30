import os
import string
import random
import tempfile
import click
# used for Ethereum account management and interaction with Ethereum wallets
from utils import *

default_password_length = 32



@click.command()
@click.option('--miners')
@click.option('--clients')
@click.option('--data-dir')
@click.option('--password-length')
def create_accounts(miners, clients, data_dir, password_length):
  accounts = {
    'owner': {},
    'miners': {},
    'clients': {}
  }

  enodes = []
  miner_addresses = []

  ## create account for owner
  password = create_random_string(password_length)
  address = create_account(password, data_dir)
  accounts['owner'][address] = password

  os.makedirs(f'{data_dir}/geth/')

  _, enode = create_keys(f'nodekey_{address}', 'rpc-endpoint-1', data_dir)
  enodes.append(enode)

  if not isinstance(miners, int):
      try:
          miners = int(miners)
      except ValueError:
          # Handle invalid input gracefully (e.g., raise custom exception or use a default)
          raise ValueError("Invalid miners number type")
  ## create accounts for miners
  for i in range(0, miners):
    password = create_random_string(password_length)
    address = create_account(password, data_dir)
    accounts['miners'][address] = password
    
    address, enode = create_keys(f'nodekey_{address}', f'validator-{i+1}', data_dir)
    ## saving enode and address serves in peers discorvery
    enodes.append(enode)
    miner_addresses.append(address)

  if not isinstance(clients, int):
      try:
          clients = int(clients)
      except ValueError:
          # Handle invalid input gracefully (e.g., raise custom exception or use a default)
          raise ValueError("Invalid clients number type")
  # create accounts for trainers or FL clients
  for i in range(0, clients):
    password = create_random_string(password_length)
    address = create_account(password, data_dir)
    accounts['clients'][address] = password

  ## saving the generated accounts with there passwords into a file
  save_json(os.path.join(data_dir, 'accounts.json'), accounts)
  ## saving miners addresses generated from bootnode keygen into a file
  save_json(os.path.join(data_dir, 'miners.json'), miner_addresses)
  ## saving enodes of geth-rpc-endpoint and geth-miners into a file
  save_json(os.path.join(data_dir, 'geth', 'static-nodes.json'), enodes)


create_accounts()
