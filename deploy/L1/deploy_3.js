async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const MyContract = await ethers.getContractFactory("Operator");
    const myContract = await MyContract.deploy("0xbe683D961487eDace67E74Fa9f6C80aD9be09e26","0x8A91DC2D28b689474298D91899f0c1baF62cB85b");
    const contract_address=  await myContract.getAddress();
    // console.log("Deployed address:" + myContract.address);
    console.log("contract deployed to:", contract_address);
  }


  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
  