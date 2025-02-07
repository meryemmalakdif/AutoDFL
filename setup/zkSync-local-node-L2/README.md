<!-- Use the "Markdown Preview" for better readability -->
# zkSync local development setup

This repository contains the tooling necessary to bootstrap zkSync locally.

## Dependencies

To run zkSync locally, you must have `docker compose` and `Docker` installed on your machine. 

## Usage

To bootstrap zkSync locally, just run:

```
> docker compose up or ./start.sh
```

This command will bootstrap three docker containers:
- Postgres (used as the database for zkSync).
- Local Geth node (used as L1 for zkSync).
- zkSync server itself.

*Note, that it is important that the first start script goes uninterrupted. If you face any issues after the bootstrapping process unexpectedly stopped, you should [reset](#resetting-zksync-state) the local zkSync state and try again.* 

## Resetting zkSync state

To reset the zkSync state, just run:

```
> docker compose down --volumes or ./clear.sh
```

This command will stop and remove all of the pods and named volumes that contains the network state

After this, you can run again:

```
> docker compose up or ./start.sh
```

## Rich wallets

Local zkSync setup comes with some "rich" wallets with large amounts of ETH on both L1 and L2.

The full list of the addresses of these accounts with the corresponding private keys can be found [here](./rich-wallets.json).

Also, during the initial bootstrapping of the system, several ERC-20 contracts are deployed locally. Note, that large quantities of these ERC-20 belong to the wallet `0x36615Cf349d7F6344891B1e7CA7C72883F5dc049` (the first one in the list of the rich wallet). Right after bootstrapping the system, these ERC-20 funds are available only on L1.

## Local testing example

You can an example of hardhat project that utilizes local testing capabilities [here](https://github.com/matter-labs/tutorial-examples/tree/main/local-setup-testing).

To run tests, clone the repo and run `yarn test`:

```
git clone https://github.com/matter-labs/tutorial-examples.git
cd local-setup-testing
yarn test
```
## For the sake of monitoring
The Geth image used in zkSync is customized and lacks the necessary monitoring ports. To enable them:
1. Build your own image by running the command below. This image is based on the original one from matterlabs/geth found in /bin/geth-entry.sh, with monitoring ports enabled:
```
> docker build -t my-custom-geth-image .
```


