import { deployContract } from "../../utils";


export default async function () {
  const contractArtifactName = "SafeMath";
  await deployContract(contractArtifactName);
}

