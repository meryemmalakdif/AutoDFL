  import { deployContract } from "./utils";

  // An example of a basic deploy script
  // It will deploy a Greeter contract to selected network
  // as well as verify it on Block Explorer if possible for the network
  export default async function () {
    const contractArtifactName = "APIConsumer";
    const constructorArguments = ["0x4abF2b3Efd541b01f8FfFDF4C4743237149e6D6b","0xDCf4717Bd9786E72c35a32972541D15644bC3e9c"];
    await deployContract(contractArtifactName,constructorArguments);
  }
  