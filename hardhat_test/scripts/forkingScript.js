const { ethers } = require("hardhat");

async function main() {
  console.log("Starting to fork...");

  await hre.network.provider.request({
    method: "hardhat_reset",
    params: [{
      forking: {
        jsonRpcUrl: "http://127.0.0.1:8545",
      }
    }]
  });

  console.log("Fork successful!");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});