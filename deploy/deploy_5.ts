import { deployContract } from "./utils";

// An example of a basic deploy script
// It will deploy a Greeter contract to selected network
// as well as verify it on Block Explorer if possible for the network
export default async function () {
  const contractArtifactName = "ManageReputation";
  // const constructorArguments = ["0x15B0B07266a6e168b2dEA0315ABD2caa678b2B26"];
  await deployContract(contractArtifactName);
}

// yarn hardhat deploy-zksync --script deploy-my-contract.ts
