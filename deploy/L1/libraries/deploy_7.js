async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const MyContract = await ethers.getContractFactory("contracts/system-contracts/libraries/FixedPointMath.sol:FixedPointMath");
    const myContract = await MyContract.deploy();
    const contract_address=  await myContract.getAddress();
    console.log("MyContract deployed to:", contract_address);
  }


  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
  