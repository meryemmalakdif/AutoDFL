<!-- Use the "Markdown Preview" for better readability -->

## Contracts Deployment

![](https://img.shields.io/badge/Note-Important-red)

To facilitate smooth interaction between contracts, it is essential to carefully consider the deployment order. Since each contract needs the address of the other one to interact effectively, the deployment sequence becomes crucial for establishing the necessary dependencies.

To ensure proper contract interaction, follow this deployment order:
1.  Deploy the `AccessManagement` contract first.
2.  Once the `AccessManagement` contract is deployed and its address is obtained, deploy the `businessLogic` contract by providing the address of the `AccessManagement` contract as a parameter.
3.  After successfully deploying the `businessLogic`, you can proceed to deploy the `manageRep` contract, providing the addresses of both the `AccessManagement` and `businessLogic` contracts as parameters.

By adhering to this deployment order, you establish the required connections between contracts, enabling them to effectively interact with one another. Failing to follow this order may result in incorrect or incomplete contract interactions, leading to potential issues within the system. Therefore, it is crucial to carefully manage the deployment process to ensure a well-connected and fully functional smart contract ecosystem.

*** To deploy on contracts on layer 1 run:
```
> npx hardhat compile
> npx hardhat run deploy/deploy_i.js
```

*** To deploy on contracts on layer 2 run:
```
> npx hardhat compile
> npx hardhat deploy-zksync --script deploy_i.ts
```
