import { deployContract } from "./utils";

// An example of a basic deploy script
// It will deploy a Greeter contract to selected network
// as well as verify it on Block Explorer if possible for the network
export default async function () {
  const contractArtifactName = "ManageReputation";
  const constructorArguments = ["0x27e04247e0a7Ba1123d660B7f3A2D3710f3749Ed"];
  await deployContract(contractArtifactName,constructorArguments);
}

// yarn hardhat deploy-zksync --script deploy-my-contract.ts
