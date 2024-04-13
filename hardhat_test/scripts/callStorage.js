async function main() {
    // Get the contract factory and deploy the contract
    const Storage = await ethers.getContractFactory("Storage");
    const storage = await Storage.deploy();
    await storage.deployed(); 

    // Store a value
    await storage.store(123);

    // Call the retrieve function using eth_call
    const value = await storage.callStatic.retrieve();
    console.log("Retrieved Value:", value.toString());
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});