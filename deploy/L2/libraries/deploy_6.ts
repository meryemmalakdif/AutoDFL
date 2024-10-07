import { deployContract } from "../../utils";

export default async function () {
  const contractArtifactName = "FixedPointMath";
  await deployContract(contractArtifactName);
}

