<!-- Use the "Markdown Preview" for better readability -->

### Create System's services Network 
This command creates a Docker network named 'BCFL' with a bridge type and assigns it the IP address range 172.16.240.0/20.
```bash
./main.sh create_docker_network
```
### Single layered blockchain

This command creates accounts necessary for the blockchain network:

- **Function**: `create_accounts`
- **Parameters**: 
  - `4` - Number of accounts for validators
  - `4` - Number of accounts for trainers
  - `15` - Passphrase length (in characters)
  - `datadir` - Directory where blockchain-related files (such as the keystore and Geth) are stored

To execute the command, run:

```bash
./main.sh create_accounts
```
This command does the same thing, but for a task publisher :
```bash
./main.sh create_account_task_publisher
```

The following command updates the balance of each account to 1,000,000,000,000,000,000,000 as needed for interactions with the blockchain.
```bash
./main.sh update_accounts_balance
```
Build a custom image for the blockchain node
```bash
./main.sh build_bc_node_image
```
This command starts the blockchain containers, taking 4 as the number of network validators and 4444 as the specified chain ID from the genesis file.
```bash
./main.sh start_bc_containers
```
This command connects to peers using the previously created network ID as the parameter.
```bash
./main.sh connect_peers
```
### Federated Learning Setup 

This command authorizes the oracle node as a sender.
- **Parameters**: 
    - Operator Contract Address: 0xc2E286Dd195B87F29bd6456DaD18f6DcAaE033A
    2. Contract ABI:  Operator Operator
    3. Oracle Node Address: 0x8CA5DAdA4E0646b6594eb538779303cB10809C72.

```bash
./main.sh authorize_operator
```
This command is used to build a custom image for the federated learning node, simulating all the functionalities that a trainer and a task publisher can have.
```bash
./main.sh build_fl_node_image
```
This command generates local datasets for 1,000 trainers.
- **Parameters**: 
    -   Number of Trainers: 1000
    -   Level of Heterogeneity: 0.5
    -   Data Storage Folder: ../../federated_learning/regular_user/data_manipulation/data/
```bash
./main.sh split_data
```
This command allows trainers to register into the BFL system.
- **Parameters**: 
    -   Contract Address: 0xC75F57411183A7294Bb109CF9f3114740d70d4D1
    -   Contract Name: BusinessLogic
    -   Contract ABI: businessLogic
    -   Number of Trainers: 5
```bash
./main.sh register_trainers
```
This command allows a task requester to publish a task
- **Parameters**:
    -   Contract Address: 0xC75F57411183A7294Bb109CF9f3114740d70d4D1
    -   Contract ABI: businessLogic BusinessLogic
    -   Rounds Number (for the sake of testing): 12
    -   Trainers Number: 5"
```bash
./main.sh start_task_publisher_containers
```
This command allows trainers to subscribe to a training task and triggers the simulation of the federated learning process, including trainer selection, training, model evaluation, and reputation update

- **Parameters**:
    -   BusinessLogic Contract Address: 0xC75F57411183A7294Bb109CF9f3114740d70d4D1
    -   BusinessLogic ABI : BusinessLogic businessLogic

    -   Reputation Contract Address: 0xf20c4bEbd07368578Db26f814b9934f22F9aa8E9
    -   Reputation ABI: ManageReputation manageRep
    -   API Consumer (for evaluation) Address: 0x4d03f9ea7806BFe9BB32cc3b0a47A3Ece2a0FFaE
    -   API Consumer ABI: APIConsumer APIconsumer
    -   Number of Trainers: 5
    -   Task ID: 1

```bash
./main.sh start_trainers_containers
```
