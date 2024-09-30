import subprocess
import json
from eth_account import Account
import string
import random
import tempfile
import os

# execution of shell commands within a Python script and capturing their output
def run_and_output(command):
  p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  (stdout, stderr) = p.communicate()
  p_status = p.wait()

  if p_status != 0:
    print(stderr)
    exit(p_status)

  return stdout.decode()

def read_json(filename):
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

def save_json(filename, data):
  json_string = json.dumps(data, indent=2)
  with open(filename, 'w') as outfile:
    outfile.write(json_string)


def create_random_string(length):
  print("length " , length)
      # Convert password_length to integer (if not already)
  if not isinstance(length, int):
      try:
          length = int(length)
      except ValueError:
          # Handle invalid input gracefully (e.g., raise custom exception or use a default)
          raise ValueError("Invalid password length provided")
  characters = string.ascii_letters + string.digits
  result_str = ''.join(random.choice(characters) for i in range(length))
  return result_str

## automates the process of creating an Ethereum account
def create_account(password, data_dir):
  with tempfile.NamedTemporaryFile() as fp:
    fp.write(password.encode())
    fp.seek(0)

    out = run_and_output(f'geth --datadir {data_dir} account new --password {fp.name}')
    ## get the public @ of the created account 
    return out.split("Public address of the key:")[1].split('\n')[0].strip()

## sets up a node for participation in the Ethereum network by generating necessary cryptographic keys
def create_keys(nodekey, host, data_dir):
  nodekey_file = os.path.join(data_dir, 'geth', nodekey)
  # generates a key that is used by bootnodes to establish their identity within the Ethereum network
  run_and_output(f'bootnode -genkey {nodekey_file}')

  with open(nodekey_file, 'r') as f:
    privkey = f.read()
    account = Account.from_key(privkey)

  # retrieves the public key (address) from a specified node key file
  pubkey = run_and_output(f'bootnode -nodekey {nodekey_file} -writeaddress').strip()
  enode = f'enode://{pubkey}@{host}:30303'
  print(enode)
  address = account.address
  return address, enode
