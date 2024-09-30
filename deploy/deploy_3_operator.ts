  import { deployContract } from "./utils";

  // An example of a basic deploy script
  // It will deploy a Greeter contract to selected network
  // as well as verify it on Block Explorer if possible for the network
  export default async function () {
    const contractArtifactName = "Operator";
    const constructorArguments = ["0x4abF2b3Efd541b01f8FfFDF4C4743237149e6D6b","0xE90E12261CCb0F3F7976Ae611A29e84a6A85f424"];
    await deployContract(contractArtifactName,constructorArguments);
  }
  
  // yarn hardhat deploy-zksync --script deploy-my-contract.ts
  