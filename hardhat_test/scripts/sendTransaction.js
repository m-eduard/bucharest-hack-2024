function encodeFunctionCall(functionSignature, parameters) {
    const iface = new ethers.utils.Interface([functionSignature]);
    return iface.encodeFunctionData(iface.functions[Object.keys(iface.functions)[0]].name, parameters);
}

async function main() {
    const provider = new ethers.providers.JsonRpcProvider();
    const signer = provider.getSigner();

    const storageAddress = process.env.STORAGE_ADDRESS;
    const functionCall = process.env.FUNCTION_CALL || "count";
    let encodedData = "";
    if (functionCall == "store") {
        let randNum = Math.floor(Math.random() * 100);
        encodedData = encodeFunctionCall("function store(uint256 num)", [randNum]);
    } else if (functionCall == "count") {
        encodedData = encodeFunctionCall("function count()", []);
    }

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