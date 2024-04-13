const fs = require('fs');

function generateConfig(numNodes) {
  let config = `require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.4",
  networks: {
    hardhat: {
      hardfork: "london",
      chains: {
        31337: {
          hardforkHistory: {
            london: 0
          }
        }
      }
    },`;

  for (let i = 1; i <= numNodes; i++) {
    config += `
    local${i}: {
      url: 'http://127.0.0.1:${8544 + i}',
      hardfork: "london"
    },`;
  }

  config = config.slice(0, -1);

  config += `
  },
};`;

  return config;
}

const numNodes = process.argv[2] ? parseInt(process.argv[2], 10) : 3;
const configFileContent = generateConfig(numNodes);

fs.writeFile('hardhat.config.js', configFileContent, (err) => {
  if (err) {
    console.error('Error writing the file:', err);
  } else {
    console.log('Config file generated successfully.');
  }
});