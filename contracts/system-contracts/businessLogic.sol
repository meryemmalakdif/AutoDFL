// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0 <0.9.0;


contract BusinessLogic {

    struct Update {
        uint trainingAccuracy;
        uint trainingDataPoints;
        string weights;
    }

    struct Score {
        address trainer;
        uint256 score;
    }

    struct Trainer {
        address _trainerAddr;
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


    uint256 _roundsDifference = 4;
    uint _scale = 1000000;
    uint256 _scaleRep = 1e18;
    uint256 _repScale = 1e26;


    // Registration Details
    mapping(address => bool) public registeredTaskPublishers;
    address[] public taskPublishers;
    address[] public trainers;    
    mapping(address => bool) public registeredTrainers;

    // here the rounds array elements corresponds to the end/finishing round before measuring the performance and updating the reputation
    // example trainer a => 2,4,6,12 => means that the trainer participated in rounds 0,1,2,3,4,5,10,11
    // assuming here that the rounds difference is 4 ie clients reselction occurs each 4 rounds
    mapping(uint => mapping(address => uint[])) public taskSelectedTrainers; // Task => trainer => rounds he has been involved in

    // Updates Details
    mapping(uint => mapping(uint => uint)) updatesCount; // task => round => number of Submited Updates
    mapping(uint => mapping(uint => mapping(address => bool))) updatesSubmitted; // task => round => Address => Bool
    mapping(uint => mapping(uint => mapping(address => Update))) public updates; // task => round => Address => Update


    // keep track of a specific publisher's interactions
    mapping(address => uint256) public publisherInteractions; // publisher => interactions

    mapping(address => mapping(address => uint256)) public interactionsTrainerWithPublisher; // trainer => publisher => interactions
    // Reputation Details
    Trainer[] public accountsReputation; // address => reputation

    // Scores Details
    mapping(uint => mapping(uint => Score[])) public scores; // task => round => Score[]


    mapping(address => uint256) public balances;

    // Dynamic array to store tasks
    Task[] public tasks;



    constructor() {
    }

    // function to register a task publisher
    function registerTaskPublisher() public {
        require(!registeredTaskPublishers[msg.sender],"Task publisher already registered.");
        taskPublishers.push(msg.sender);
        registeredTaskPublishers[msg.sender] = true;
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
                currentRound: 0,
                maxRounds: maxRounds,
                requiredTrainers: requiredTrainers,
                registeredTrainers: new address[](0),
                state: "selection"
            })
        );
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
        require(registeredTrainers[msg.sender] == true, "the trainer is not registered in the bcfl system , he can't ask to join a task");
        Task storage task = tasks[_taskId];
        require(isInAddressArray(task.registeredTrainers, msg.sender) == false,"the trainer has already joined the task");
        task.registeredTrainers.push(msg.sender);
    }

   


    // assigns a trainer to a specific task
    function setTaskTrainers(uint _taskId, address[] memory taskTrainers) public {
        require(_taskId + 1 <= tasks.length, "Task does not exist");
        Task storage task = tasks[_taskId];
        // require(task.publisher == msg.sender, "Only the publisher can select trainers");
        publisherInteractions[task.publisher] += taskTrainers.length;
        for (uint i = 0; i <= taskTrainers.length - 1; i++) {
            interactionsTrainerWithPublisher[taskTrainers[i]][task.publisher] += 1; 
        }
        task.trainers= taskTrainers;
        task.state = "training";
           
    }



    function getTrainersForTask(uint256 _taskId) external view returns (address[] memory) {
        require(_taskId < tasks.length,"Invalid task ID: Task does not exist.");
        return tasks[_taskId].trainers;
    }

    // I think hadi is enough
    function isTrainerForTask(uint _taskId,address addr) public view returns (bool) {
        require(_taskId < tasks.length, "Task does not exist");
        return isInAddressArray(tasks[_taskId].trainers, addr);
    }

        // all interactions a trainer has with a specific publisher 
    function historicalInteractions(address _taskPublisher,address _addr) public view returns (uint256) {
        return interactionsTrainerWithPublisher[_addr][_taskPublisher];
    }

    // total number of the tasks a trainer has participated in
    function totalNumberOfTasks(address addr) public view returns (uint256) {
              uint256 _totalTasks = 0;
     if(registeredTrainers[addr] == true)
      {
        for (uint i = 0; i < tasks.length; i++) {
            if (isTrainerForTask(i, addr) == true) {
                _totalTasks += 1;
            }
        }
        }
        return _totalTasks;
    }


        // total number of interactions a publisher have
    function publisherTotalInteractions(address _publisher) public view returns (uint256) {
        return publisherInteractions[_publisher];
    }

    // Count the number of tasks published by the given address
    function allTasksOfTaskPublisher(address addr) public view returns (uint[] memory) {
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

    // Function to get all tasks
    function getAllTasks() public view returns (Task[] memory) {
        return tasks;
    }
    // Function to get a single task by its ID
    function getTaskById(uint256 taskId) public view returns (Task memory) {
        require(taskId < tasks.length, "Task does not exist");
        return tasks[taskId];
    }

    function submitUpdate(Update memory modelUpdate,uint task,uint _round) public  {
        require(updatesSubmitted[task][_round][msg.sender] == false,"The sender already submitted updates for this running round");
        Task storage task_details = tasks[task];
        updates[task][_round][msg.sender] = modelUpdate;
        updatesSubmitted[task][_round][msg.sender] = true;
        updatesCount[task][_round]++;
        if (updatesCount[task][_round] == task_details.trainers.length) {
            task_details.state = "evaluation";
        }
    }

    function submitScore(uint _task,uint _round,Score[] memory _scores) public   {
        for (uint i = 0; i < _scores.length; i++) {
            scores[_task][_round].push(_scores[i]);
        }
        Task storage task_details = tasks[_task];
        task_details.state = "aggregation";
    }

    function getRoundScores(uint _taskId,uint _round) public returns (Score[] memory) {
        Score[] memory _scores = new Score[](scores[_taskId][_round].length);
        for (uint256 i = 0; i < scores[_taskId][_round].length; i++) {
            _scores[i] = scores[_taskId][_round][i];
        }
        return _scores;
    }

    function getAllTrainers() public returns (address[] memory) {
        return trainers;
    }

    function getUpdatesForAggregationTask(uint taskId,uint _round) public  returns (string[] memory)  {
        string[] memory taskUpdates = new string[](tasks[taskId].trainers.length);
        for (uint i = 0; i < tasks[taskId].trainers.length; i++) {
            taskUpdates[i] = updates[taskId][_round][tasks[taskId].trainers[i]].weights;
        }
        return (taskUpdates);
    }

    function UpdateGlobalModelWeights(uint _taskId,string memory globalModelWeightsCID) public  {
        require(_taskId + 1 <= tasks.length, "Task does not exist");
        tasks[_taskId].globalModelWeightsCID = globalModelWeightsCID;
        tasks[_taskId].currentRound++;
    }

    function updateTaskState(uint _taskId, string memory _state) public  {
        require(_taskId + 1 <= tasks.length, "Task does not exist");
        Task storage task = tasks[_taskId];
        task.state = _state;
    }

    function getTaskState(uint _taskId) public returns (string memory) {
        require(_taskId < tasks.length, "Task does not exist");
        return tasks[_taskId].state;
    }

    function isInAddressArray(address[] memory arr, address look) public view returns (bool) {
    bool found = false;
     if(arr.length>0)    
          {  for (uint i = 0; i < arr.length; i++) {
      if (arr[i] == look) {
        found = true;
        break;
      }
    }}
    return found;
  } 



    function setReputation(address _addr, uint256 _newRep) public  {
        for (uint i = 0; i < accountsReputation.length; i++) {
            if (accountsReputation[i]._trainerAddr == _addr) {
                accountsReputation[i]._reputation = _newRep;
                break;
            }
        }
    }

    function getReputation(address _addr) public  returns (uint256) {
        uint256 _rep;
        for (uint i = 0; i < accountsReputation.length; i++) {
            if (accountsReputation[i]._trainerAddr == _addr) {
                _rep = accountsReputation[i]._reputation;
                break;
            }
        }
        return _rep;
    }

    function getAllReputations() public  view returns (Trainer[] memory) {
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
