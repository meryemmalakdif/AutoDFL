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
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "param1",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "param2",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "param3",
        "type": "string"
      }
    ],
    "name": "AllAggregationsSubmitted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "round",
        "type": "uint256"
      }
    ],
    "name": "AllWeightSubmitted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "task",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "round",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "behaviour",
            "type": "uint256"
          }
        ],
        "indexed": false,
        "internalType": "struct MainContract.Score[]",
        "name": "scores",
        "type": "tuple[]"
      }
    ],
    "name": "EvaluationDone",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "modelCID",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "infoCID",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "publisher",
        "type": "address"
      }
    ],
    "name": "TaskPublished",
    "type": "event"
  },
  {
    "anonymous": false,
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
            "name": "testingAccuracy",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "indexed": false,
        "internalType": "struct MainContract.Update",
        "name": "submission",
        "type": "tuple"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "trainer",
        "type": "address"
      }
    ],
    "name": "WeightSubmitted",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "aggregatorIsRegistered",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "round",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "roundsNumber",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "globalModelWeightsCID",
        "type": "string"
      }
    ],
    "name": "globalModelUpdated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [],
    "name": "reachedAllowedTrainers",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address[]",
        "name": "",
        "type": "address[]"
      }
    ],
    "name": "startTrainingRound",
    "type": "event"
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
      },
      {
        "internalType": "string",
        "name": "_state",
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
    "name": "aggregations",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
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
    "name": "aggregationsTask",
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
    "name": "aggregators",
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
    "inputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "trainer",
            "type": "address"
          },
          {
            "internalType": "uint256[]",
            "name": "rounds",
            "type": "uint256[]"
          }
        ],
        "internalType": "struct MainContract.Item[]",
        "name": "array",
        "type": "tuple[]"
      },
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "filterTrainer",
    "outputs": [
      {
        "internalType": "int256",
        "name": "",
        "type": "int256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getAggregators",
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
        "name": "_taskId",
        "type": "uint256"
      }
    ],
    "name": "getAggregatorsForTask",
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
        "internalType": "struct MainContract.Trainer[]",
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
            "internalType": "bool",
            "name": "isPublished",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isCompleted",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isVerified",
            "type": "bool"
          },
          {
            "internalType": "address[]",
            "name": "trainers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "aggregators",
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
            "internalType": "uint256",
            "name": "requiredAggregators",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "registeredTrainers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "registeredAggregators",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "state",
            "type": "string"
          }
        ],
        "internalType": "struct MainContract.Task[]",
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
    "inputs": [],
    "name": "getRoundForTraining",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "",
        "type": "string"
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
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "getRoundScores",
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
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "_trainer",
        "type": "address"
      }
    ],
    "name": "getScoreWorker",
    "outputs": [
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
    "stateMutability": "nonpayable",
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
        "internalType": "address",
        "name": "task_trainer",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "getSingleUpdate",
    "outputs": [
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "trainingAccuracy",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "testingAccuracy",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct MainContract.Update",
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
            "internalType": "bool",
            "name": "isPublished",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isCompleted",
            "type": "bool"
          },
          {
            "internalType": "bool",
            "name": "isVerified",
            "type": "bool"
          },
          {
            "internalType": "address[]",
            "name": "trainers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "aggregators",
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
            "internalType": "uint256",
            "name": "requiredAggregators",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "registeredTrainers",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "registeredAggregators",
            "type": "address[]"
          },
          {
            "internalType": "string",
            "name": "state",
            "type": "string"
          }
        ],
        "internalType": "struct MainContract.Task",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTrainers",
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
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "getTrainersForTaskRound",
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
        "internalType": "address[]",
        "name": "",
        "type": "address[]"
      },
      {
        "components": [
          {
            "internalType": "uint256",
            "name": "trainingAccuracy",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "testingAccuracy",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct MainContract.Update[]",
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
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "taskTrainers",
        "type": "address[]"
      }
    ],
    "name": "gettestit",
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
    "name": "god",
    "outputs": [
      {
        "internalType": "address",
        "name": "trainer",
        "type": "address"
      }
    ],
    "stateMutability": "view",
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
    "name": "interactionTaskPublisherTrainer",
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
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "isAggregatorForTask",
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
        "internalType": "uint256[]",
        "name": "arr",
        "type": "uint256[]"
      },
      {
        "internalType": "uint256",
        "name": "look",
        "type": "uint256"
      }
    ],
    "name": "isInIntArray",
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
        "internalType": "uint256",
        "name": "taskId",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "trainerAddress",
        "type": "address"
      }
    ],
    "name": "isTrainerInTask",
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
    "inputs": [],
    "name": "model",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
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
    "inputs": [],
    "name": "registerAggregator",
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
    "name": "registerAggregatorTask",
    "outputs": [],
    "stateMutability": "nonpayable",
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
    "inputs": [],
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
    "name": "registeredAggregators",
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
    "inputs": [],
    "name": "round",
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
    "name": "roundPhase",
    "outputs": [
      {
        "internalType": "enum MainContract.RoundPhase",
        "name": "",
        "type": "uint8"
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
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "behaviour",
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
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "selectedAggregators",
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
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "selectedTrainers",
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
        "name": "taskAggregators",
        "type": "address[]"
      }
    ],
    "name": "setTaskAggregators",
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
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "taskTrainers",
        "type": "address[]"
      }
    ],
    "name": "setTaskRoundTrainers",
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
        "internalType": "string",
        "name": "_weights",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "task",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "task_aggregators",
        "type": "address[]"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "submitAggregation",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          },
          {
            "internalType": "uint256",
            "name": "behaviour",
            "type": "uint256"
          }
        ],
        "internalType": "struct MainContract.Score[]",
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
            "name": "testingAccuracy",
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
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct MainContract.Update",
        "name": "modelUpdate",
        "type": "tuple"
      },
      {
        "internalType": "uint256",
        "name": "task",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "task_trainers",
        "type": "address[]"
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
        "internalType": "string",
        "name": "modelUpdate",
        "type": "string"
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
    "name": "submitUpdatee",
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
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "taskParticipationLevel",
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
    "name": "taskks",
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
        "internalType": "string",
        "name": "state",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "requiredTrainers",
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
        "internalType": "bool",
        "name": "isPublished",
        "type": "bool"
      },
      {
        "internalType": "bool",
        "name": "isCompleted",
        "type": "bool"
      },
      {
        "internalType": "bool",
        "name": "isVerified",
        "type": "bool"
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
        "internalType": "uint256",
        "name": "requiredAggregators",
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
        "internalType": "uint256",
        "name": "_taskId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      },
      {
        "internalType": "address[]",
        "name": "taskTrainers",
        "type": "address[]"
      }
    ],
    "name": "testit",
    "outputs": [],
    "stateMutability": "nonpayable",
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
        "name": "testingAccuracy",
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
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
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
        "name": "task",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "_round",
        "type": "uint256"
      }
    ],
    "name": "updatesTask",
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
    "name": "updatess",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
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
    "name": "weights",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
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
const CONTRACT_ADDRESS = "0x4abF2b3Efd541b01f8FfFDF4C4743237149e6D6b";

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

  const startTime = new Date().getTime();
  var data = fs.readFileSync("../BusinessLogic-benchmarks/workload/submitUpdate.json");
  var data= JSON.parse(data);
  let currentNonce = await wallet.getNonce();
  currentNonce;
  let transactionPromises = [];
  numTransactions = 100;

  const updates = [{
    trainingAccuracy: 0.9, 
    testingAccuracy: 0.8, 
    trainingDataPoints: 17, 
    weights: "some_hash", 
    timestamp: 1724045954183
}] ;

  for (let i = 0; i < numTransactions ; i++) {

    let task = data[i].task ; 
    let trainers = data[i].trainers ; 
    let round = data[i].round ; 
    var tx = await contract.submitUpdatee("some_hash", task, round );

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