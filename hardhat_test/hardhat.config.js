require("@nomiclabs/hardhat-waffle");

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
    },
    local1: {
      url: 'http://127.0.0.1:8545',
      hardfork: "london"
    },
    local2: {
      url: 'http://127.0.0.1:8546',
      hardfork: "london"
    },
    local3: {
      url: 'http://127.0.0.1:8547',
      hardfork: "london"
    }
  },
};