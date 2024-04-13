function encodeFunctionCall(functionSignature, parameters) {
    const iface = new ethers.utils.Interface([functionSignature]);
    return iface.encodeFunctionData(iface.functions[Object.keys(iface.functions)[0]].name, parameters);
}

async function main() {
    const provider = new ethers.providers.JsonRpcProvider(); // Connect to your provider
    const signer = provider.getSigner(); // Ensure the signer is configured correctly in your Hardhat setup

    const storageAddress = "0x5fbdb2315678afecb367f032d93f642f64180aa3"; // Replace with your deployed contract address
    const encodedData = encodeFunctionCall("function store(uint256 num)", [123]); // Replace 123 with your desired number

    const tx = {
        to: storageAddress,
        data: encodedData,
    };

    const response = await signer.sendTransaction(tx);
    console.log("Transaction response:", response);
    await response.wait();
    console.log("Transaction confirmed in block:", response.blockNumber);
}

main().catch((error) => {
    console.error("Error:", error);
    process.exit(1);
});