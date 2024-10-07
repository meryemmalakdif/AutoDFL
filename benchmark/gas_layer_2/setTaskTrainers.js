const startTimeH = new Date().getTime();
const { Wallet, Provider } = require("zksync-web3");
const ethers = require("ethers");
let fs = require('fs');


// load env file

// load contract artifact. Make sure to compile first!
const abi = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "globalModelWeightsCID",
        "type": "string"
      }
    ],
    "name": "UpdateGlobalModelWeights",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "accountsReputation",
    "outputs": [
      {
        "internalType": "address",
        "name": "_trainerAddr",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_reputation",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "allTasksOfTaskPublisher",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "balances",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "deposit",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllReputations",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "_trainerAddr",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "_reputation",
            "type": "uint256"
          }
        ],
        "internalType": "struct BusinessLogic.Trainer[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllTasks",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "taskId",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "modelCID",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "infoCID",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "publisher",
            "type": "address"
          },
          {
            "internalType": "address[]",
            "name": "trainers",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "globalModelWeightsCID",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "currentRound",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxRounds",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requiredTrainers",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "registeredTrainers",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "state",
            "type": "string"
          }
        ],
        "internalType": "struct BusinessLogic.Task[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAllTrainers",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "",
        "type": "address[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_addr",
        "type": "address"
      }
    ],
    "name": "getBalance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_addr",
        "type": "address"
      }
    ],
    "name": "getReputation",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "getRoundScores",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "trainer",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "score",
            "type": "uint256"
          }
        ],
        "internalType": "struct BusinessLogic.Score[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      }
    ],
    "name": "getTaskById",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "taskId",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "modelCID",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "infoCID",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "publisher",
            "type": "address"
          },
          {
            "internalType": "address[]",
            "name": "trainers",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "globalModelWeightsCID",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "currentRound",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "maxRounds",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "requiredTrainers",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "registeredTrainers",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "state",
            "type": "string"
          }
        ],
        "internalType": "struct BusinessLogic.Task",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      }
    ],
    "name": "getTaskState",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      }
    ],
    "name": "getTrainersForTask",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "",
        "type": "address[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "getUpdatesForAggregationTask",
    "outputs": [
      {
        "internalType": "string[]",
        "name": "",
        "type": "string[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_taskPublisher",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_addr",
        "type": "address"
      }
    ],
    "name": "historicalInteractions",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "interactionsTrainerWithPublisher",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address[]",
        "name": "arr",
        "type": "address[]"
      },
      {
        "internalType": "address",
        "name": "look",
        "type": "address"
      }
    ],
    "name": "isInAddressArray",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "isTrainerForTask",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_modelCID",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_infoCID",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "maxRounds",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "requiredTrainers",
        "type": "uint256"
      }
    ],
    "name": "publishTask",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "publisherInteractions",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_publisher",
        "type": "address"
      }
    ],
    "name": "publisherTotalInteractions",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "registerTaskPublisher",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "adr",
        "type": "address"
      }
    ],
    "name": "registerTrainer",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      }
    ],
    "name": "registerTrainerTask",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "registeredTaskPublishers",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "registeredTrainers",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "scores",
    "outputs": [
      {
        "internalType": "address",
        "name": "trainer",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "score",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_addr",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_newRep",
        "type": "uint256"
      }
    ],
    "name": "setReputation",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "taskTrainers",
        "type": "address[]"
      }
    ],
    "name": "setTaskTrainers",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_task",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "trainer",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "score",
            "type": "uint256"
          }
        ],
        "internalType": "struct BusinessLogic.Score[]",
        "name": "_scores",
        "type": "tuple[]"
      }
    ],
    "name": "submitScore",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "trainingAccuracy",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "trainingDataPoints",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "weights",
            "type": "string"
          }
        ],
        "internalType": "struct BusinessLogic.Update",
        "name": "modelUpdate",
        "type": "tuple"
      },
      {
        "internalType": "uint256",
        "name": "task",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "submitUpdate",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "taskPublishers",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "taskSelectedTrainers",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "tasks",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "modelCID",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "infoCID",
        "type": "string"
      },
      {
        "internalType": "address",
        "name": "publisher",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "globalModelWeightsCID",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "currentRound",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "maxRounds",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "requiredTrainers",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "state",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "totalNumberOfTasks",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_publisher",
        "type": "address"
      }
    ],
    "name": "totalNumberOfTasksWithPublisher",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "_publisher",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      }
    ],
    "name": "totalNumberOfTasksWithPublisherTask",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "totalParticipationLevel",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "trainers",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "_state",
        "type": "string"
      }
    ],
    "name": "updateTaskState",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "updates",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "trainingAccuracy",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "trainingDataPoints",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "weights",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
];

const PRIVATE_KEY = "0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110";

if (!PRIVATE_KEY)
  throw "⛔️ Private key not detected! Add it to the .env file!";

// Address of the contract on zksync testnet
const CONTRACT_ADDRESS = "0x79e8C120BfDD3F820149b0179498cD947476bEF4";

if (!CONTRACT_ADDRESS) throw "⛔️ Contract address not provided";

// An example of a deploy script that will deploy and call a simple contract.
async function main() {
  const startTimeH = new Date().getTime();
  console.log(`Running script to interact with contract ${CONTRACT_ADDRESS}`);

  // Initialize the provider.
  const provider = new Provider("http://127.0.0.1:3050");
  const signer = new ethers.Wallet(PRIVATE_KEY, provider);
  const wallet = new Wallet("0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110", provider);


  // Initialize contract instance
  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    abi,
    signer
  );

  // send transaction to add another owner
  const startTime = new Date().getTime();
  var data = fs.readFileSync("../BusinessLogic-benchmarks/workload/scripts/setTaskTrainersData.json");
  var data= JSON.parse(data);
  let currentNonce = await wallet.getNonce();
  currentNonce;
  let transactionPromises = [];
  numTransactions = 100;

  for (let i = 0; i < numTransactions ; i++) {
    let task =data[i].task
    let taskTrainers = data[i].taskTrainers ; 
    var tx = await contract.setTaskTrainers(task, taskTrainers);

  
    // transactionPromises.push(tx);

  }
  console.log("Waiting for transactions to be mined...");
  // const transactions = await Promise.all(transactionPromises);

  // console.log("Checking transaction receipts...");
  // const receipts = await Promise.all(transactions.map(tx => tx.wait()));
  
  const endTime = new Date().getTime();
  console.log(startTime)
  console.log(endTime)
  const timeDiff = endTime - startTime;
  console.log(timeDiff);
  
}

 

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});