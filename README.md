### Welcome to AutoDFL: A Scalable and Automated Reputation-Aware Decentralized Federated Learning

### Repository Structure

- `benchmark/`: This directory contains the code and tools used in the benchmarking and testing phase .
- `contracts/`: Here, you can find the smart contract code for the: proposed model, business logic, and external systems interactions like Oracles.
- `deploy/`:  scripts that manage smart contracts deployements.
- `monitor/`: designated directory for scripts and files related to monitoring and tracking functionalities. It provides a ready monitoring environment to collect and visualize geth metrics with prometheus and grafana. it can be configured for both L1 and L2.
- `/federated_learning`**: all the modules that allow the simulation of the federated learning (Training data, training module , aggregation modules, evaluation modules).
- `scripts/`: This folder includes the scripts necessary to run the system's containers (Like the FL nodes).
- `setup/`: Contains the initial configuration and installation process required to run the whole framework (BC-Client
Chainlink / ZkSync / FL nodes) nodes.


### How to Use This Repository

If you wish to reproduce the experiments or explore the code, please refer to the detailed documentation provided in each directory. The `README.md` files in individual folders will guide you through the setup and usage of the respective components.

### Citation 

Please consider citing our paper and project if they help your research.
@article{dif2025autodfl,
  title={AutoDFL: A Scalable and Automated Reputation-Aware Decentralized Federated Learning},
  author={Dif, Meryem Malak and Bouchiha, Mouhamed Amine and Rabah, Mourad and Ghamri-Doudane, Yacine},
  journal={arXiv preprint arXiv:2501.04331},
  year={2025}
}

