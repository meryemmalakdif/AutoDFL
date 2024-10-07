import { deployContract } from "../utils";


export default async function () {
  const contractArtifactName = "BusinessLogic";
  // const constructorArguments = ["0xf05f74BB750f6272BE8B1b4Ea180184f61c22f84"];
  await deployContract(contractArtifactName);
}

