<!-- Use the "Markdown Preview" for better readability -->
# L1 Blockchain Infrastructure

This folder contains the necessary infrastructure for running a single-layer blockchain.

## Setup Instructions
For the sake of repository organization, all the necessary scripts for setting up a single-layered blockchain are located in the scripts/bash folder.
```bash
cd ../scripts/bash
```
1. Create accounts for validators and clients (users interacting with the blockchain).
   ```bash
   ./main.sh create_accounts
2. Update their balance
   ```bash
    ./main.sh update_accounts_balance
3. Set up an isolated network environment where the blockchain nodes (validators) and other services (like oracles or clients) can connect
    ```bash
     ./main.sh create_docker_network
    ```
4. Build the blockchain validators images
    ```bash
     ./main.sh build_bc_node_image
    ```
5. Launches Docker containers running the validator software for the blockchain. Each validator node participates in the consensus process, validating transactions and blocks 
    ```bash
     ./main.sh start_bc_containers
    ```
6. Connects the started validator nodes to each other, allowing them to share information about transactions and blocks
    ```bash
     ./main.sh connect_peers
    ```
