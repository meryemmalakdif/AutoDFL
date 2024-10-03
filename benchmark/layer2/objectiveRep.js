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
    "name": "_overallNegativeHistory",
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
    "name": "_overallPositiveHistory",
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
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "_taskPublisher",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_trainers",
        "type": "address[]"
      },
      {
        "internalType": "uint256[]",
        "name": "_scores",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256[]",
        "name": "totalRounds",
        "type": "uint256[]"
      }
    ],
    "name": "calculateObjectiveReputation",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      },
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
        "internalType": "address",
        "name": "_taskPublisher",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_trainers",
        "type": "address[]"
      },
      {
        "internalType": "uint256",
        "name": "_interactionsTp",
        "type": "uint256"
      },
      {
        "internalType": "uint256[]",
        "name": "_interactionsTpTa",
        "type": "uint256[]"
      }
    ],
    "name": "calculateSubjectiveReputation",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "int256",
        "name": "x",
        "type": "int256"
      }
    ],
    "name": "calculateTanhLambdaX",
    "outputs": [
      {
        "internalType": "int256",
        "name": "",
        "type": "int256"
      }
    ],
    "stateMutability": "pure",
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
        "name": "_taskPublisher",
        "type": "address"
      },
      {
        "internalType": "address[]",
        "name": "_trainers",
        "type": "address[]"
      },
      {
        "internalType": "uint256[]",
        "name": "_scores",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256[]",
        "name": "totalRounds",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256",
        "name": "maxRounds",
        "type": "uint256"
      },
      {
        "internalType": "uint256[]",
        "name": "_subjectiveRep",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256[]",
        "name": "_objectiveRep",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256",
        "name": "_goodBehaviourThreshold",
        "type": "uint256"
      },
      {
        "internalType": "uint256[]",
        "name": "_prevRep",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256[]",
        "name": "totalNumberOfTasksWithPublisher",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256[]",
        "name": "interactions",
        "type": "uint256[]"
      }
    ],
    "name": "updateReputation",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

const PRIVATE_KEY = "0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110";

if (!PRIVATE_KEY)
  throw "⛔️ Private key not detected! Add it to the .env file!";

// Address of the contract on zksync testnet
const CONTRACT_ADDRESS = "0x5e0bC5f3a4948A8Dd4F2660D32CDcA81C1Dc7367";

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
  var data = fs.readFileSync("../ReputationModel-benchmarks/workload/objectiveReputationData.json");
  var data= JSON.parse(data);
  let currentNonce = await wallet.getNonce();
  currentNonce;
  let transactionPromises = [];
  numTransactions = 1;

  for (let i = 0; i < numTransactions ; i++) {
    let taskId = data[i].taskId ; 
    let taskPublisher = data[i].taskPublisher ; 
    let trainers = data[i].trainers ; 
    let scores= data[i].scores ; 
    let totalRounds = data[i].totalRounds ; 

    var tx = await contract.calculateObjectiveReputation(taskId, taskPublisher,trainers,scores,totalRounds);

  
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