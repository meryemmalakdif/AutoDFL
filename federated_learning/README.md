<!-- Use the "Markdown Preview" for better readability -->

# Federated Learning

This folder contains the necessary modules and components for implementing federated learning in a decentralized system.

## Folder Structure

- **oracle_external_adapter/**
  - This folder contains the Oracle External Adapter, which runs through a Python server. It enables Chainlink oracles to perform custom functionalities  that are not built-in, such as evaluating models and aggregating results from different trainers.
- **regular_user/**
  - Contains components relevant to regular users participating in the federated learning process, allowing them to publish training tasks as task requesters and manage the training of local models as trainers.

## Key Features

- **Task Publishing**: Allows for the efficient submission and management of training tasks by publishers.
- **Model Training**: Facilitates the training of local models by multiple trainers, ensuring data remains decentralized and secure.
- **Evaluation and Aggregation**: Utilizes the Oracle External Adapter to evaluate the performance of local models and aggregate the results into a global model, enabling Chainlink oracles to execute functionalities beyond their built-in capabilities.
