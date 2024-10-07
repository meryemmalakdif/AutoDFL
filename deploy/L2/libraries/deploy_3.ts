import { deployContract } from "../../utils";


export default async function () {
  const contractArtifactName = "Math";
  await deployContract(contractArtifactName);
}

