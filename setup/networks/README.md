<!-- Use the "Markdown Preview" for better readability -->

# Networks Folder

This folder contains the configuration and files necessary for setting up the network infrastructure of the blockchain system.

## Folder Structure

- **docker/**
  - Contains Dockerfiles for building necessary images.
    - `Dockerfile.bcNode`: Dockerfile for the blockchain node.
    - `Dockerfile.flNode`: Dockerfile for the federated learning node.
  
- **docker-compose/**
  - Contains YAML files for managing multi-container Docker applications.
- **middlewares/**
  - Contains Python scripts for middleware functionalities to run the blockchain network like creating accounts , updating their balance , connecting peers...

