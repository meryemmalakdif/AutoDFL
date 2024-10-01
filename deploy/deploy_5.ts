import { deployContract } from "./utils";

// An example of a basic deploy script
// It will deploy a Greeter contract to selected network
// as well as verify it on Block Explorer if possible for the network
export default async function () {
  const contractArtifactName = "ManageReputation";
  const constructorArguments = ["0xBE6Fc9B483329b65e7be1747a7B12193820e8654"];
  await deployContract(contractArtifactName,constructorArguments);
}

// yarn hardhat deploy-zksync --script deploy-my-contract.ts
