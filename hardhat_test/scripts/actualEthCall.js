function getFunctionSelector(functionSignature) {
    return ethers.utils.keccak256(ethers.utils.toUtf8Bytes(functionSignature)).slice(0, 10); // first 4 bytes (8 characters + '0x')
}



async function main() {
    const [signer] = await ethers.getSigners();
    const provider = signer.provider;

    const storageAddress = "0x5fbdb2315678afecb367f032d93f642f64180aa3";

    const callData = getFunctionSelector("retrieve()");
    // const callData = getFunctionSelector("store(uint256)") + ethers.utils.defaultAbiCoder.encode(["uint256"], [123]).slice(2);
    
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