import { deployContract } from "../utils";

export default async function () {
  const contractArtifactName = "ManageReputation";
  const constructorArguments = ["0x79e8C120BfDD3F820149b0179498cD947476bEF4"];
  await deployContract(contractArtifactName,constructorArguments);
}

