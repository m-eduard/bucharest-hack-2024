function getFunctionSelector(functionSignature) {
    return ethers.utils.keccak256(ethers.utils.toUtf8Bytes(functionSignature)).slice(0, 10);
}

async function main() {
    const [signer] = await ethers.getSigners();
    const provider = signer.provider;

    const storageAddress = process.env.STORAGE_ADDRESS;

    const callData = getFunctionSelector("retrieve()");
    
    const transaction = {
        to: storageAddress,
        data: callData
    };

    const result = await provider.send("eth_call", [transaction, "latest"]);
    const value = ethers.BigNumber.from(result).toString();

    console.log("Value retrieved:", value);
}

main().catch((error) => {
    console.error(error);
    process.exit(1);
});