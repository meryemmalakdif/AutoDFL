import { deployContract } from "./utils";

// An example of a basic deploy script
// It will deploy a Greeter contract to selected network
// as well as verify it on Block Explorer if possible for the network
export default async function () {
  const contractArtifactName = "ManageReputation";
  const constructorArguments = ["0x6E6bc3D438d0f4Fb61c2141c97F008507E7bb183"];
  await deployContract(contractArtifactName,constructorArguments);
}

// yarn hardhat deploy-zksync --script deploy-my-contract.ts
