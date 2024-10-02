import { deployContract } from "./utils";

// An example of a basic deploy script
// It will deploy a Greeter contract to selected network
// as well as verify it on Block Explorer if possible for the network
export default async function () {
  const contractArtifactName = "ManageReputation";
  const constructorArguments = ["0x29f3C506E29Ce1799dcd705bf5cfE62bc1f9B01f"];
  await deployContract(contractArtifactName,constructorArguments);
}

// yarn hardhat deploy-zksync --script deploy-my-contract.ts
