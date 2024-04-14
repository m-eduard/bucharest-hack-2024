require("@nomiclabs/hardhat-waffle");

module.exports = {
  solidity: "0.8.4",
  networks: {
    hardhat: {
      hardfork: "london",
      chains: {
        31337: {
          hardforkHistory: {
            london: 1
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
    },
    local4: {
      url: 'http://127.0.0.1:8548',
      hardfork: "london"
    },
    local5: {
      url: 'http://127.0.0.1:8549',
      hardfork: "london"
    },
    local6: {
      url: 'http://127.0.0.1:8550',
      hardfork: "london"
    },
    local7: {
      url: 'http://127.0.0.1:8551',
      hardfork: "london"
    },
    local8: {
      url: 'http://127.0.0.1:8552',
      hardfork: "london"
    },
    local9: {
      url: 'http://127.0.0.1:8553',
      hardfork: "london"
    },
    local10: {
      url: 'http://127.0.0.1:8554',
      hardfork: "london"
    }
  },
};