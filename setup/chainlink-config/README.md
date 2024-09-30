<!-- Use the "Markdown Preview" for better readability -->
##  Oracle Setup Instructions
Oracle Chainlink Node Setup Instructions
This document outlines the steps to configure and run an Oracle Chainlink node. Follow the instructions carefully to ensure a successful setup.

Starting the Database and Network
To start the PostgreSQL database and run the Chainlink network, execute the following commands:
  ```bash
    ./run_postgress.sh
    ./run_chainlink.sh
```
Create a bridge for three routes:
  - **evaluation (/)**
  - **aggregation (./aggregation)**
  - **preRepComputation (./preReputation)**.

Create three jobs (details in folder ./jobs) using the oracle UI.

Add the **Link token**, providing the link to the oracle and **apiConsumer**.

Authorize the address of the oracle by running the command:
  ```bash
    cd ../../scripts
    ./main.sh authorize_operator
```
  