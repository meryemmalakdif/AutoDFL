async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const MyContract = await ethers.getContractFactory("APIConsumer");
    const myContract = await MyContract.deploy("0xbe683D961487eDace67E74Fa9f6C80aD9be09e26","0xD4DC4279550c46aC7C77B3F85d63641C1F48E9d7");
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
  