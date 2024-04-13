async function main() {
    const [deployer] = await ethers.getSigners();
  
    console.log("Deploying contracts with the account:", deployer.address);
  
    const Storage = await ethers.getContractFactory("Storage");
    const storage = await Storage.deploy();
  
    console.log("Storage contract deployed to:", storage.address);
  }
  
  main().catch((error) => {
    console.error(error);
    process.exit(1);
  });