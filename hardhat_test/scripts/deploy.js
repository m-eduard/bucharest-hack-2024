async function main() {
    const [deployer] = await ethers.getSigners();
  
    console.log("Deploying contracts with the account:", deployer.address);

    const contractInput = process.env.CONTRACT;
  
    const Contract = await ethers.getContractFactory(contractInput);
    const contract = await Contract.deploy();
  
    console.log(contractInput, " contract deployed to:", contract.address);
  }
  
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });