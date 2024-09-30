import json
import click
from utils import *

def get_enodes(network):
  ## the next two lines are equavalent to this docker network inspect network_name | jq '.[0].Containers' , get all the containers within a docker network 
  output = run_and_output(f'docker network inspect {network}')
  containers = json.loads(output)[0]['Containers']
  enodes = {}

  for container in containers:
    # IPv4 address assigned to the container within the specified subnet
    ip = containers[container]['IPv4Address']
    ip = ip.split('/')[0] # Remove that part of an ip@ eg 10.10.0.2/20 . removes 20

    enode = run_and_output(f'docker exec -it {container} geth --exec "console.log(admin.nodeInfo.enode)" attach')
    enode = enode.split('\n')[0]
    enode = enode.strip()
    # .replace(old_string,new_string)
    # once we generated enode we used host machine @ as ip @ , it should be chnaged to the docker container ip@ so it can be accessed from other containers ?????
    enode = enode.replace('127.0.0.1', ip)
    print(ip)

    enodes[container] = enode

  return enodes

def connect_enodes(enodes):
  for container in enodes:
    for peer in enodes:
      run_and_output(f'docker exec -it {container} geth --exec "admin.addPeer(\'{enodes[peer]}\')" attach')

  
@click.command()
@click.option('--network')
def connect_bc_network(network):
  print(network)
  connect_enodes(get_enodes(network))


connect_bc_network()
