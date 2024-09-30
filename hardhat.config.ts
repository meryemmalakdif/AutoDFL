import { HardhatUserConfig } from "hardhat/config";


require("@nomiclabs/hardhat-ethers");
require("@nomicfoundation/hardhat-verify");

import "@matterlabs/hardhat-zksync";
import "@matterlabs/hardhat-zksync-deploy";
import "@matterlabs/hardhat-zksync-solc";

const config: HardhatUserConfig = {
  defaultNetwork: "dockerizedNode",
  networks: {
    dockerizedNode: {
      url: "http://127.0.0.1:3050",
      ethNetwork: "http://127.0.0.1:8545",
      zksync: true,
    },
    inMemoryNode: {
      url: "http://127.0.0.1:8011",
      ethNetwork: "localhost", // in-memory node doesn't support eth node; removing this line will cause an error
      zksync: true,
    },
    hardhat: {
      zksync: true,
    },
  },
  zksolc: {
    version: "latest",
    settings: {
      // find all available options in the official documentation
      // https://era.zksync.io/docs/tools/hardhat/hardhat-zksync-solc.html#configuration
        libraries: {
              "contracts/Math.sol": {
                "Math": "0xf20c4bEbd07368578Db26f814b9934f22F9aa8E9"
              },
              "contracts/FixedPointMath.sol": {
                "FixedPointMath": "0x9ED5Dd59f1DAA698DD0dd00D9560704cf9C13De6"
              }
            }
    },
  },
  solidity: {
    compilers: [
      {
        version: "0.8.24",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      },
      {
        version: "0.5.5",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      },
      {
        version: "0.8.19",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      },
      {
        version: "0.7.6",
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      },
      {
        version: "0.6.7",
        //settings: {},
        settings: {
          optimizer: {
            enabled: true,
            runs: 200
          }
        }
      },
    ],
  },
};

export default config;
