import os
import click
# used for Ethereum account management and interaction with Ethereum wallets
from eth_account import Account
from utils import *


@click.command()
@click.option('--src')
@click.option('--dst')
@click.option('--consensus')
@click.option('--balance')
@click.option('--data-dir')
def update_accounts_balance(src, dst, consensus, balance, data_dir):
  genesis = read_json(src)
  genesis['alloc'] = {}
  accounts = read_json(os.path.join(data_dir, 'accounts.json'))
  ## allocating some ether to each account , usefull for contract deployment of interactions with smart contracts
  for account in accounts['miners']:
    genesis['alloc'][account] = { 'balance': balance }

  for account in accounts['clients']:
    genesis['alloc'][account] = { 'balance': balance }

  for account in accounts['owner']:
    genesis['alloc'][account] = { 'balance': balance }
  for account in accounts['taskpublishers']:
    genesis['alloc'][account] = { 'balance': balance }

  if consensus == 'poa':
    extra_data = '0x0000000000000000000000000000000000000000000000000000000000000000'
    for account in list(accounts['miners']):
      extra_data += account[2:]
    extra_data += '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    genesis['extraData'] = extra_data
    
  save_json(dst, genesis)



update_accounts_balance()