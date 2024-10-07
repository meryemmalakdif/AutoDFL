async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const MyContract = await ethers.getContractFactory("ManageReputation");
    const myContract = await MyContract.deploy("0x0bb74468691928bD65600C65CC58D5fc010b7066");
    const contract_address=  await myContract.getAddress();
    // console.log("Deployed address:" + myContract.address);
    console.log("manage reputation contract deployed to:", contract_address);
  }


  
  main()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
  