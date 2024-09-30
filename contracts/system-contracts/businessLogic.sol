// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;

import "@openzeppelin/contracts/utils/Strings.sol";

contract BusinessLogic  {
  // imported contracts



      function concatenate(string[] memory parts) internal pure returns (string memory) {
        bytes memory result;

        for (uint256 i = 0; i < parts.length; i++) {
            result = abi.encodePacked(result, parts[i],"-");
        }

        return string(result);
    }

 // Helper function to convert address to string
    function addressToString(address _addr) internal pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_addr)));
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(42);
        str[0] = '0';
        str[1] = 'x';
        for (uint256 i = 0; i < 20; i++) {
            str[2 + i * 2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3 + i * 2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }
        return string(str);
    }
    // Function to concatenate an array of addresses
function concatenateAddresses(address[] memory addresses) internal pure returns (string memory) {
    bytes memory result;

    for (uint256 i = 0; i < addresses.length; i++) {
        result = abi.encodePacked(result, addressToString(addresses[i]), "-");
    }

    return string(result);
}




  struct Update {
    uint trainingAccuracy;
    uint testingAccuracy;
    uint trainingDataPoints;
    string weights;
    uint256 timestamp;
  }

  struct Score {
    address trainer ;
    uint256 score;
    uint256 behaviour;
  }

  struct Trainer {
    address _trainerAddr ;
    uint256 _reputation;
  }


  
  struct Task {
    uint taskId;
    string modelCID;
    string infoCID;
    //string testDataset;
    //uint256 requiredFinalAccuracy;
    address publisher;
    address[] trainers;
    string globalModelWeightsCID;
    uint currentRound;
    uint maxRounds;
    uint requiredTrainers;
    address[] registeredTrainers;
    string state;

  }






  enum RoundPhase {
    Stopped,
    WaitingForUpdates,
    WaitingForAggregations,
    WaitingForTermination
  }
  uint256 _roundsDifference = 4 ;
  uint _scale = 1000000 ;
  uint256 _scaleRep = 1e18 ;
  uint256 _repScale = 1e26 ;

  // Initialization Details
  address public owner;
  string  public model;     // IPFS CID for model encoded as h5.
  RoundPhase afterUpdate;   // Which phase is executed after WaitingForUpdates.

  // Registration Details
  address[]                 public taskPublishers;
  mapping(address => bool) public registeredTaskPublishers;
  address[]                 public trainers;
  mapping(address => bool)  public registeredTrainers;

  // Round Details
  uint                        public round = 0;
  RoundPhase                  public roundPhase = RoundPhase.Stopped;
  mapping(uint => string)     public weights;             // Round => Weights ID
  mapping(uint => address[])  public selectedTrainers;    // Round => Trainers for the round


  // here the rounds array elements corresponds to the end/finishing round before measuring the performance and updating the reputation
  // example trainer a => 2,4,6,12 => means that the trainer participated in rounds 0,1,2,3,4,5,10,11
  // assuming here that the rounds difference is 2 ie clients reselction occurs each 2 rounds
  mapping(uint=>mapping(address => uint[]))  public taskSelectedTrainers;    // Task => trainer => rounds he has been involved in  


    struct Item {
        address trainer;
        uint[] rounds;
    }
      mapping(uint=>Item[])  public god;    // Task => trainer => rounds he has been involved in  


  // Updates Details
  mapping(uint => mapping(uint => uint)) updatesCount;                           // task => round => number of Submited Updates
  mapping(uint => mapping(uint => mapping(address => bool))) updatesSubmitted;   // task => round => Address => Bool
  mapping(uint => mapping(uint => mapping(address => Update))) public updates;   // task => round => Address => Update


  // Reputation Details
  Trainer[] public accountsReputation;   // address => reputation

  // Scores Details
  mapping(uint => mapping(uint => uint)) scoresCount;                           // task => round => number of Submited scores
  //mapping(uint => mapping(uint => mapping(address => bool))) updatesSubmitted;   // task => round => Address => Bool
  mapping(uint => mapping(uint => Score[])) public scores;   // task => round => Score[]


  // Aggregations Details
  mapping(uint => mapping(uint => uint))                       aggregationsCount;        // task => round => number of Submited Aggregations
  mapping(uint => mapping(uint => mapping(address => bool)))   aggregationsSubmitted;    // task => Round => Address => Bool
  mapping(uint => mapping(uint => mapping(address => string))) public aggregations;      // Round => Address => Weights ID
  mapping(uint => mapping(uint => mapping(string => uint)))    aggregationsResultsCount; // task => Round => Weights ID => Count
  mapping(address => uint256) public balances;


  // Dynamic array to store tasks
  Task[] public tasks;

  event TaskPublished(uint256 taskId, string modelCID, string infoCID, address publisher);
  event WeightSubmitted(Update submission, address trainer);
  event AllWeightSubmitted(uint taskId, uint round);
  event AllAggregationsSubmitted(uint indexed param1, uint indexed param2, string param3);

  event aggregatorIsRegistered(uint);
  event globalModelUpdated(uint indexed round , uint roundsNumber,  string globalModelWeightsCID);
  event reachedAllowedTrainers();
  event startTrainingRound(address[]);
  event EvaluationDone(uint task, uint round, Score[] scores);


  //constructor(address _accesManagementContractAddress, address _apiConsumerContractAddress, string memory _model, string memory _weights, RoundPhase _afterUpdate) {
    constructor(){
    }

 

  // function to register a task publisher
  function registerTaskPublisher() public {
      if (registeredTaskPublishers[msg.sender] == false) {
        taskPublishers.push(msg.sender);
        registeredTaskPublishers[msg.sender] = true;
      }
    }


    // set the trainers for a specific task for a specific time slot 
  function testit(uint _taskId , uint _round, address[] memory taskTrainers) public {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    // taskSelectedTrainers[_taskId][taskTrainers[0]] = new uint[](0);
    taskSelectedTrainers[_taskId][taskTrainers[0]].push(_round+2);
  }

  function gettestit(uint _taskId, address[] memory taskTrainers) public view returns (uint[] memory) {
      require(_taskId+1 <= tasks.length, "Task does not exist");
      // mapping(address => uint[]) memory _taskTrainers = taskSelectedTrainers[_taskId];
      return  taskSelectedTrainers[_taskId][taskTrainers[0]];
  }

  // Function to publish a task
  function publishTask(string memory _modelCID, string memory _infoCID, uint maxRounds, uint requiredTrainers) public {
      uint256 taskId = tasks.length; // Get the index of the newly added task
      tasks.push(Task({
          taskId: taskId,
          modelCID: _modelCID,
          infoCID: _infoCID,
          publisher: msg.sender,
          trainers: new address[](0),
          globalModelWeightsCID: "",
          currentRound:0,
          maxRounds: maxRounds,
          requiredTrainers: requiredTrainers,
          registeredTrainers: new address[](0),
          state: "selection"
      }));
  }
  
  function registerTrainer() public {
    if (registeredTrainers[msg.sender] == false) {
      trainers.push(msg.sender);
      registeredTrainers[msg.sender] = true;
      Trainer memory newTrainer;
      newTrainer._trainerAddr = msg.sender;
      newTrainer._reputation = 500000000000;
      Trainer[] storage _accountsRep = accountsReputation ;
      _accountsRep.push(newTrainer);
    }
  }

  // registers a trainer to a specific task
  function registerTrainerTask(uint _taskId) public {
    require(_taskId < tasks.length, "Task does not exist");
    require(registeredTrainers[msg.sender] == true , "the trainer is not registered in the bcfl system , he can't ask to join a task");      
    Task storage task = tasks[_taskId];
    require(isInAddressArray(task.registeredTrainers,msg.sender) == false , "the trainer has already joined the task");      
    task.registeredTrainers.push(msg.sender);
  }

  // assigns a trainer to a specific task
  function setTaskTrainers(uint _taskId, address[] memory taskTrainers) public {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    Task storage task = tasks[_taskId];
    require(task.publisher == msg.sender, "Only the publisher can select trainers");
    for (uint i = 0; i < taskTrainers.length; i++) {
      require(isInAddressArray(task.registeredTrainers,taskTrainers[i]) == true , "the trainer is not registered in the task");      
      require(task.requiredTrainers > task.trainers.length, "Already reached required number of trainers , u can not be selected to this task to this task");
      task.trainers.push(taskTrainers[i]);
    if (task.trainers.length == task.requiredTrainers) {
          task.state = "training";
    } 
    }
  }


     function filterTrainer(Item[] memory array , address addr) public view returns (int ) {
      int index = -1 ;
      for (uint i = 0; i < array.length; i++) {
          if (array[i].trainer == addr)
          {
              index = int(i) ;
          }
      }
      return index ;
     }

  //   // set the trainers for a specific task for a specific time slot 
  // function setTaskRoundTrainers(uint _taskId, uint _round , address[] memory taskTrainers) public {
  //   require(_taskId+1 <= tasks.length, "Task does not exist");
  //   if (_round == 0){
  //     god[_taskId] = new Item[](0);
  //   }
  //   uint[] storage _rounds = [];
  //   Task storage task = tasks[_taskId];
  //   for (uint i = 0; i < taskTrainers.length; i++) {
  //     require(isInAddressArray(task.registeredTrainers,taskTrainers[i]) == true , "the trainer is not registered in the task");  
  //     int index = filterTrainer(god[_taskId] ,taskTrainers[i] ) ;
  //     if (index == -1){
  //       _rounds.push(_round+2) ;
  //       // add the trainer to the task's mapping
  //       god[_taskId].push(Item(taskTrainers[i],_rounds));
  //       god[_taskId][0].rounds.push(_round+2); 
  //     }else{
  //       god[_taskId][uint(index)].rounds.push(_round+2); 
  //     }
  //     // Item[] storage itemIds = god[_taskId];
  //     // uint[] storage itemRounds = itemIds[1].rounds ;
  //     // itemRounds.push(_round+2);
  //     // god[_taskId].push(Item(taskTrainers[i], itemRounds)); 

  //     if(isInAddressArray(task.trainers,taskTrainers[i]) == false){
  //         task.trainers.push(taskTrainers[i]);
  //     }
  //   }
  //   task.state = "training";
  // }

    // set the trainers for a specific task for a specific time slot 
  function setTaskRoundTrainers(uint _taskId, uint _round , address[] memory taskTrainers) public {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    Task storage task = tasks[_taskId];
    if (_round == 0){
      tasks[_taskId].trainers = taskTrainers ;
      }

    for (uint i = 0; i < taskTrainers.length; i++) {
      require(isInAddressArray(task.registeredTrainers,taskTrainers[i]) == true , "the trainer is not registered in the task");  
      // if (taskSelectedTrainers[_taskId][taskTrainers[i]].length == 0) {

      //   taskSelectedTrainers[_taskId][taskTrainers[i]] = new uint[](0);
      //   }

        taskSelectedTrainers[_taskId][taskTrainers[i]].push(_round+2);
      // if the current trainer is new for the current task => add its address to the task's trainers struct
 
      if(isInAddressArray(task.trainers,taskTrainers[i]) == false){
          tasks[_taskId].trainers.push(taskTrainers[i]);
      }

   



    }
    task.state = "training";
  }


  function getTrainersForTaskRound(uint _taskId, uint _round) public view  returns (address[] memory) {
      require(_taskId+1 <= tasks.length, "Task does not exist");
      // mapping(address => uint[]) memory _taskTrainers = taskSelectedTrainers[_taskId];
      address[] memory _roundChosenTrainers = new address[](tasks[_taskId].requiredTrainers);  
      uint _index = 0 ;
      for (uint i = 0; i < tasks[_taskId].trainers.length; i++){
         // if ( isInIntArray(taskSelectedTrainers[_taskId][tasks[_taskId].trainers[i]],_round+2) == true ) {
            _roundChosenTrainers[_index] = tasks[_taskId].trainers[i];
            _index++ ;
         // }
      }
      return _roundChosenTrainers;
  }



  function getTrainersForTask(uint _taskId) external view returns (address[] memory) {
        require(_taskId+1 <= tasks.length, "Task does not exist");

        return tasks[_taskId].trainers;
    }




  function isTrainerForTask(uint _taskId, address addr) public view returns (bool) {
        require(_taskId+1 <= tasks.length, "Task does not exist");
        return isInAddressArray(tasks[_taskId].trainers, addr);
    }



  function interactionTaskPublisherTrainer(address _taskPublisher , address _addr) public view returns (uint256) {
        //require(_taskId+1 <= tasks.length, "Task does not exist");
        require(registeredTrainers[_addr]==true, "Trainer is not registered in the system");
        uint256 _totalInteractions = 0 ;
        for (uint i = 0; i <= tasks.length-1; i++) {
          // u need to consider in each task the level of participation too 
          if ( tasks[i].publisher == _taskPublisher && isTrainerInTask(i,_addr) ){
            _totalInteractions += taskParticipationLevel(i,_addr) ;
          }         
        }
        return _totalInteractions;
    }

      function historicalInteractions(address _taskPublisher , address _addr , uint taskId) public view returns (uint256) {
        //require(_taskId+1 <= tasks.length, "Task does not exist");
        require(registeredTrainers[_addr]==true, "Trainer is not registered in the system");
        uint256 _totalInteractions = 0 ;
        for (uint i = 0; i <= tasks.length-1; i++) {
          // u need to consider in each task the level of participation too 
          if ( tasks[i].publisher == _taskPublisher && isTrainerInTask(i,_addr) && tasks[i].taskId != taskId  ){
            _totalInteractions += taskParticipationLevel(i,_addr) ;
          }         
        }
        return _totalInteractions;
    }

  function isTrainerInTask(uint taskId, address trainerAddress) public view returns (bool) {
    mapping(address => uint[]) storage trainersForTask = taskSelectedTrainers[taskId];
    uint[] memory trainerList = trainersForTask[trainerAddress];
    return trainerList.length > 0;
    }


  function taskParticipationLevel(uint _taskId, address addr) public view returns (uint256) {
        require(_taskId+1 <= tasks.length, "Task does not exist");
        require(registeredTrainers[addr]==true, "Trainer is not registered in the system");
        uint256 _totalRounds = 0 ;
        for (uint i = 1; i <= taskSelectedTrainers[_taskId][addr].length; i++) {
        
            _totalRounds += _roundsDifference;
          
        }
        return _totalRounds;
    }


  function totalParticipationLevel(address addr) public view returns (uint256) {
        require(registeredTrainers[addr]==true, "Trainer is not register in the system");
        uint256 _total = 0 ;
        for (uint i = 0; i < tasks.length; i++) {
        if( isTrainerInTask(i, addr) == true )
        {
          _total += taskParticipationLevel(i, addr) ;
        }
          }
        return _total;
    }
  function totalNumberOfTasks(address addr) public view returns (uint256) {
        require(registeredTrainers[addr]==true, "Trainer is not register in the system");
        uint256 _totalTasks = 0 ;
        for (uint i = 0; i < tasks.length; i++) {
        if( isTrainerInTask(i, addr) == true )
        {
          _totalTasks += 1 ;
        }
          }
        return _totalTasks;
    }



      function totalNumberOfTasksWithPublisher(address addr, address _publisher) public view returns (uint256) {
        require(registeredTrainers[addr]==true, "Trainer is not register in the system");
        uint256 _totalTasks = 0 ;
        for (uint i = 0; i < tasks.length; i++) {
        if( tasks[i].publisher == _publisher && isTrainerInTask(i, addr) == true)
        {
          _totalTasks += 1 ;
        }
          }
        return _totalTasks;
    }
function allTasksOfTaskPublisher(address addr) public view returns (uint[] memory) {
    // Count the number of tasks published by the given address
    uint count = 0;
    for (uint i = 0; i < tasks.length; i++) {
        if (tasks[i].publisher == addr) {
            count++;
        }
    }

    // Allocate memory for the _totalTasks array
    uint[] memory _totalTasks = new uint[](count);

    // Populate the _totalTasks array
    uint index = 0;
    for (uint i = 0; i < tasks.length; i++) {
        if (tasks[i].publisher == addr) {
            _totalTasks[index] = tasks[i].taskId;
            index++;
        }
    }

    return _totalTasks;
}




  function updatesTask(uint task, uint _round) public view returns (uint) {
        return updatesCount[task][_round];
    }

  function getTrainers() public view returns (address[] memory) {
    return trainers;
  }




  function isSelectedTrainer() internal view returns (bool) {
    return isInAddressArray(selectedTrainers[round], msg.sender);
  }


  function getRoundForTraining() public view virtual returns (uint, string memory) {
    // require(roundPhase == RoundPhase.WaitingForUpdates, "The system is not in training phase");
    // require(isSelectedTrainer(), "The trainer is not selected");
    return (round, weights[round - 1]);
  }






  // Function to get all tasks
  function getAllTasks() public view returns (Task[] memory) {
      return tasks;
  }
  // Function to get a single task by its ID
  function getTaskById(uint256 taskId) public view returns (Task memory) {
      require(taskId < tasks.length, "Task does not exist"); 
      return tasks[taskId];
  }

mapping(uint => mapping(uint => mapping(address => bool))) private trainerLocks;

  modifier trainerLock(uint task, uint _round) {
    require(!trainerLocks[task][_round][msg.sender], "Trainer has already submitted for this round");
    trainerLocks[task][_round][msg.sender] = true; // Lock the trainer
    _;
    trainerLocks[task][_round][msg.sender] = false; // Unlock after function execution
  }

uint public number ;

  // function submitUpdate(Update memory modelUpdate, uint task, address[] memory task_trainers, uint _round) public {
  //   require(updatesSubmitted[task][_round][msg.sender] == false, "The sender already submitted updates for this running round");

  //   updates[task][_round][msg.sender] = modelUpdate;
  //   updatesSubmitted[task][_round][msg.sender] = true;

  //   updatesCount[task][_round]++;

  //   if (updatesCount[task][_round] == task_trainers.length) {
  //     updateTaskState(task, "evaluation");
  //     triggerEvaluation(task, _round, "accuracy");
  //   }
  // }

bool oracleCallPending;
    function submitUpdate(Update memory modelUpdate , uint task, address[] memory task_trainers, uint _round) public virtual {
    require(updatesSubmitted[task][_round][msg.sender] == false, "The sender already submitted updates for this running round");
    Task storage task_details = tasks[task];
    updates[task][_round][msg.sender] = modelUpdate;
    updatesSubmitted[task][_round][msg.sender] = true;
    updatesCount[task][_round]++;
    if (updatesCount[task][_round] == task_trainers.length) {
task_details.state = "evaluation";

    }
  }
  


  function triggerEvaluation(uint taskId, uint _round, string memory evaluation) public{
  // require(roundPhase == RoundPhase.WaitingForAggregations, "The system is not in aggregation phase");
  // require(isSelectedAggregator() == true, "The aggregator is not selected");


   (address[] memory roundTrainers, string[] memory taskUpdates) = getUpdatesForAggregationTask(taskId,_round);
   string memory round_updates = concatenate(taskUpdates);
   string memory round_trainers = concatenateAddresses(roundTrainers);

  //  consumerContractInstance.requestVolumeData(round_updates, round_trainers , tasks[taskId].modelCID , tasks[taskId].globalModelWeightsCID ,  evaluation ,  Strings.toString(_round));

}
  function submitScore( uint _task , uint _round, Score[] memory _scores  ) public virtual {

    //require(roundPhase == RoundPhase.WaitingForScores, "The system is not waiting for scores");
    // require the one that calls this function only an admin can do this 

    for (uint i = 0; i < _scores.length; i++) {
        scores[_task][_round].push(_scores[i]);
    }
    Task storage task_details = tasks[_task];
    task_details.state = "aggregation";
  }


function getScoreWorker(uint _taskId, uint _round , address _trainer) public returns (uint256,uint256) {
  Score[] memory _scores = scores[_taskId][_round];
      for (uint256 i = 0; i < _scores.length; i++) {
      if (_scores[i].trainer == _trainer) {
          return (_scores[i].score , _scores[i].behaviour );
      }
  }
}

function getNUmber() public returns (uint) {
  return number;
}
function getRoundScores(uint _taskId, uint _round) public returns (Score[] memory) {
      Score[] memory _scores = new Score[](scores[_taskId][_round].length);
      for (uint256 i = 0; i < scores[_taskId][_round].length; i++) {
        _scores[i] = scores[_taskId][_round][i] ;
        }
        return _scores;
}


function getAllTrainers() public returns (address[] memory) {
    return trainers;
}

  
function getUpdatesForAggregationTask(uint taskId, uint _round) public returns (address[] memory , string[] memory) {
  // require(roundPhase == RoundPhase.WaitingForAggregations, "The system is not in aggregation phase");
  // require(isSelectedAggregator() == true, "The aggregator is not selected");
  address[] memory _roundTrainers = getTrainersForTaskRound(taskId,_round);
  string[] memory taskUpdates = new string[](_roundTrainers.length);
  for (uint i = 0; i < _roundTrainers.length; i++) {
    taskUpdates[i] = updates[taskId][_round][_roundTrainers[i]].weights;
  }
  return (_roundTrainers, taskUpdates);
}

function getSingleUpdate(uint taskId, address task_trainer, uint _round) public view returns (Update memory) {
  // require(roundPhase == RoundPhase.WaitingForAggregations, "The system is not in aggregation phase");
  // require(isSelectedAggregator() == true, "The aggregator is not selected");

  Update memory taskUpdate = updates[taskId][_round][task_trainer];
  return taskUpdate;
}




  function UpdateGlobalModelWeights(uint _taskId, string memory globalModelWeightsCID, string memory _state) public {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    // require(task.publisher == msg.sender, "Only the publisher can update The global model");
    tasks[_taskId].globalModelWeightsCID = globalModelWeightsCID;
    tasks[_taskId].currentRound++;
    // updateTaskState(_taskId, _state);
    
    //emit globalModelUpdated(tasks[_taskId].currentRound, tasks[_taskId].maxRounds, globalModelWeightsCID);
  }

  function updateTaskState(uint _taskId, string memory _state) public {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    // require(task.publisher == msg.sender, "Only the publisher can update The global model");
    Task storage task = tasks[_taskId];
    task.state = _state; 
    }


  function getTaskState(uint _taskId) public returns(string memory) {
    require(_taskId+1 <= tasks.length, "Task does not exist");
    // require(task.publisher == msg.sender, "Only the publisher can update The global model");
    return tasks[_taskId].state;

    }

 function isInAddressArray(address[] memory arr, address look) public view returns (bool) {
    bool found = false;
     if(arr.length>0)    
          {    for (uint i = 0; i < arr.length; i++) {
      if (arr[i] == look) {
        found = true;
        break;
      }
    }}
    return found;
  }

   function isInIntArray(uint[] memory arr, uint look) public view returns (bool) {
    bool found = false;
    for (uint i = 0; i < arr.length; i++) {
      if (arr[i] == look) {
        found = true;
        break;
      }
    }
    return found;
  }



  function setReputation(address _addr , uint256 _newRep) public {
    for (uint i=0 ; i< accountsReputation.length ; i++){
      if(accountsReputation[i]._trainerAddr == _addr){
        accountsReputation[i]._reputation = _newRep ;
        break;
      }
    }
    }

  function getReputation(address _addr) public returns (uint256) {
    uint256 _rep ; 
    for (uint i=0 ; i< accountsReputation.length ; i++){
      if(accountsReputation[i]._trainerAddr == _addr){
        _rep = accountsReputation[i]._reputation ;
        break;
      }
    }
    return _rep ;
    }

  function getAllReputations() public view returns (Trainer[] memory) {
      return accountsReputation;
  }


      function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
      }


    function getBalance(address _addr) public view returns (uint256) {
      return balances[_addr];
  }






}