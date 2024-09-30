import os
import string
import random
import tempfile
import click
# used for Ethereum account management and interaction with Ethereum wallets
from eth_account import Account
from utils import *

default_password_length = 32

@click.command()
@click.option('--data-dir')
@click.option('--password-length')
def create_account_task_publisher(data_dir,password_length):
    # Open the file in read mode
    with open(data_dir+"/accounts.json") as f:
        accounts_data = json.load(f)

    # Add (account, password) to the existing 'taskpublishers' array
    password = create_random_string(password_length)
    address = create_account(password, data_dir)
    if 'taskpublishers' not in accounts_data:
        accounts_data['taskpublishers'] = {} 
    accounts_data['taskpublishers'][address] = password

    # Save the updated JSON data back to the file
    with open(data_dir+"/accounts.json", 'w') as f:
        json.dump(accounts_data, f, indent=4)


  

create_account_task_publisher()