  import { deployContract } from "../utils";


  export default async function () {
    const contractArtifactName = "APIConsumer";
    const constructorArguments = ["0x4abF2b3Efd541b01f8FfFDF4C4743237149e6D6b","0xDCf4717Bd9786E72c35a32972541D15644bC3e9c"];
    await deployContract(contractArtifactName,constructorArguments);
  }
  