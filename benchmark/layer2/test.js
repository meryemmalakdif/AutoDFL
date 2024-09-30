const { ethers } = require("ethers");
const { Wallet, Provider } = require("zksync-web3");
let fs = require('fs');

async function runThroughputTest() {
  const provider = new Provider("http://127.0.0.1:3050");
  const wallet = new Wallet("0x7726827caac94a7f9e1b160f7ea819f172f7b6f9d2a97f992c38edeab82d4110", provider);
  ABI= [
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
              "internalType": "int256",
              "name": "score",
              "type": "int256"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
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
          "internalType": "int256[]",
          "name": "",
          "type": "int256[]"
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
          "internalType": "int256",
          "name": "",
          "type": "int256"
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
        },
        {
          "internalType": "uint256",
          "name": "requiredAggregators",
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
          "internalType": "int256",
          "name": "score",
          "type": "int256"
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
              "internalType": "int256",
              "name": "score",
              "type": "int256"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
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
  ]
  const contract = new ethers.Contract("0x919FD847a2baEfeB9696aCb95c9154f0eC9964D0", ABI, wallet);

  const numTransactions = 5;
  const results = [];
  const startTime = Date.now();
  var data = fs.readFileSync("../BusinessLogic-benchmarks/workload/workload.json");
  var data= JSON.parse(data);
  
  const sendPromises = [];
  let currentNonce = await wallet.getNonce();
  currentNonce += 1 

  for (let i = 0; i < numTransactions; i++) {
    
    let _modelCID =data[0][i]._modelCID
    let _infoCID = data[0][i]._infoCID ; 
    let maxRounds = data[0][i].maxRounds ; 
    let requiredTrainers = data[0][i].requiredTrainers ; 
    let requiredAggregators = data[0][i].requiredAggregators ; 
    sendPromises.push(sendTransaction(contract, _modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators ,currentNonce  ));
    currentNonce ++ ;
    
  }
  console.log("haha")

  const txResults = await Promise.allSettled(sendPromises);
  console.log("the end")
  const endTime = Date.now();

  const successfulTxs = txResults.filter(r => r.status === 'fulfilled');
  const failedTxs = txResults.filter(r => r.status === 'rejected');

  const successRate = (successfulTxs.length / numTransactions) * 100;
  const failureRate = (failedTxs.length / numTransactions) * 100;
  const sendRate = numTransactions / ((endTime - startTime) / 1000);
  
  const latencies = successfulTxs.map(r => r.value.latency);
  const maxLatency = Math.max(...latencies);
  const minLatency = Math.min(...latencies);
  const avgLatency = latencies.reduce((a, b) => a + b, 0) / latencies.length;
  
  const throughput = successfulTxs.length / ((endTime - startTime) / 1000);

  console.log(`Success Rate: ${successRate.toFixed(2)}%`);
  console.log(`Failure Rate: ${failureRate.toFixed(2)}%`);
  console.log(`Send Rate (TPS): ${sendRate.toFixed(2)}`);
  console.log(`Max Latency (s): ${maxLatency.toFixed(2)}`);
  console.log(`Min Latency (s): ${minLatency.toFixed(2)}`);
  console.log(`Avg Latency (s): ${avgLatency.toFixed(2)}`);
  console.log(`Throughput (TPS): ${throughput.toFixed(2)}`);
}

// async function sendTransaction(contract, _modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators) {
//   const startTime = Date.now();
//   const tx = await contract.publishTask( _modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators);
//   await tx.wait();
//   const endTime = Date.now();
//   return { latency: (endTime - startTime) / 1000 };
// }
// async function sendTransaction(contract, _modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators, maxRetries = 3) {
//     const startTime = Date.now();
//     let retries = 0;
//     while (retries < maxRetries) {
//       try {
//         const tx = await contract.publishTask(_modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators);
//         await tx.wait(2); // Wait for 2 confirmations
//         const endTime = Date.now();
//         return { latency: (endTime - startTime) / 1000 };
//       } catch (error) {
//         console.log(`Attempt ${retries + 1} failed: ${error.message}`);
//         retries++;
//         if (retries >= maxRetries) throw error;
//         await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds before retrying
//       }
//     }
//   }
  


async function sendTransaction(contract, _modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators, currentNonce) {
  const startTime = Date.now();
  const tx = await contract.publishTask(_modelCID, _infoCID, maxRounds, requiredTrainers, requiredAggregators, {
    nonce: currentNonce
  });
  await tx.wait();
  const endTime = Date.now();
  return { latency: (endTime - startTime) / 1000 };
}


runThroughputTest();
