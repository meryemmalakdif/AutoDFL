  import { deployContract } from "../utils";

  export default async function () {
    const contractArtifactName = "Operator";
    const constructorArguments = ["0x4abF2b3Efd541b01f8FfFDF4C4743237149e6D6b","0xE90E12261CCb0F3F7976Ae611A29e84a6A85f424"];
    await deployContract(contractArtifactName,constructorArguments);
  }
  
  