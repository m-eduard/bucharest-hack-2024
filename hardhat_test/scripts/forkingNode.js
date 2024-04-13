const { ethers } = require("hardhat");

async function main() {
  console.log("Starting to fork...");

  await hre.network.provider.request({
    method: "hardhat_reset",
    params: [{
      forking: {
        jsonRpcUrl: process.env.FORK_URL,
        blockNumber: Number(process.env.FORK_BLOCK_NUMBER)
      }
    }]
  });

  console.log("Fork successful!");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});