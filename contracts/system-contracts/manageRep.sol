// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./businessLogic.sol";
import "./libraries/FixedPointMath.sol";

contract ManageReputation {
    // imported libraries
    using FixedPointMath for int256;

    // Imported contracts
    BusinessLogic public taskContractInstance;

    //uint _scale = 10**17;
    uint _scale = 1000000;
    uint256 _scaleScore = 1e18; // 1000000000000000000
    uint256 _scaling = 1e14;
    uint256 _scaleDifference = _scaleScore / _scale;

    mapping(address => mapping(address => uint256)) public _overallPositiveHistory; // address TP => address trainer => value
    mapping(address => mapping(address => uint256)) public _overallNegativeHistory; // address TP => address trainer => value

    mapping(uint => mapping(address => mapping(uint => uint256))) public _roundPositivePerformance; // task id => trainer => round => + performance
    mapping(uint => mapping(address => mapping(uint => uint256))) public _roundNegativePerformance; // task id => trainer => round => - performance

    mapping(uint => mapping(address => mapping(uint => uint256))) public _totalRounds; // task id => trainer => round => + performance

    constructor(address _taskContractAddress) {
        taskContractInstance = BusinessLogic(_taskContractAddress);
    }

    function calculateTanhLambdaX(int256 x) public pure returns (int256) { 
        return x.tanhLambdaX(); 
    }

    // It is based on the historical interactions between a task publisher and a trainer
    function uncertaintyBetweenTrainerAndPublisher(address _taskPublisher, address _trainer, uint taskId) public returns (uint256) {
        uint256 _result = 0;
        uint256 _u;

        uint256 _interactionsTpTa = taskContractInstance.historicalInteractions(_taskPublisher, _trainer, taskId);
        uint256 _interactionsTp = 0;

        address[] memory _allTrainers = taskContractInstance.getAllTrainers();
        for (uint j = 0; j < _allTrainers.length; j++) {
            _interactionsTp += taskContractInstance.historicalInteractions(_taskPublisher, _allTrainers[j],taskId);
        }
        if (_interactionsTp > 0) {
            _u = _scale - ((_interactionsTpTa * _scale) / _interactionsTp); 
        }
        return _u;
    }

    function iterateMappingPositive(BusinessLogic.Task memory _taskDetails, address _addr) public view returns (uint256) {
        uint256 _result = 0;
        for (uint i = 0; i < _taskDetails.maxRounds; i++) {
            _result += _roundPositivePerformance[_taskDetails.taskId][_addr][i + 2];
        }
        return _result;
    }

    function iterateMappingNegative(BusinessLogic.Task memory _taskDetails, address _addr) public view returns (uint256) {
        uint256 _result = 0;
        for (uint i = 0; i < _taskDetails.maxRounds; i++) {
            _result += _roundNegativePerformance[_taskDetails.taskId][_addr][i + 2];
        }
        return _result;
    }

    // Reputation updates occur at the end of each timeslot, which is composed of multiple training rounds
    function updateReputation(uint _taskId, uint _startingRound, uint _finishingRound, address[] memory _trainers, uint256[] memory _scores, uint256[] memory totalRounds) public {
        uint historical = 0;
        BusinessLogic.Task memory _taskDetails = taskContractInstance.getTaskById(_taskId);
        address _taskPublisher = _taskDetails.publisher;
        uint256 _prevRep;
        uint256 _newRep;
        uint256 _localRep;
        uint _threshold = (_trainers.length * 2) / 3;
        uint256 _weight;
        uint256 _weight_local_rep;
        uint256 _uncertainty_weight;
        uint256 _subjectiveRep;
        uint256 _goodBehaviourThreshold = 0;

        for (uint j = 0; j <= _threshold - 1; j++) {
            _goodBehaviourThreshold = _goodBehaviourThreshold + _scores[j];
        }
        _goodBehaviourThreshold = _goodBehaviourThreshold / _threshold;

        uint256 _objectiveRep;

        for (uint j = 0; j < _trainers.length; j++) {
            _objectiveRep = 0;
            // Update for the coming rounds and tasks
            if ((_scores[j] + 150000000000000000) >= _goodBehaviourThreshold) {
                _roundPositivePerformance[_taskId][_trainers[j]][_finishingRound] += _scores[j] * _finishingRound;
                _objectiveRep = (_scale * _scale * totalRounds[j]) / 4;
            } else {
                _roundNegativePerformance[_taskId][_trainers[j]][_finishingRound] += _scores[j] * _finishingRound;
                _objectiveRep = (4 * _scale * _scale * totalRounds[j]) / 40;
            }

            // Calculate subjective reputation
            if (taskContractInstance.totalNumberOfTasksWithPublisher(_trainers[j], _taskDetails.publisher) > 1) {
                // a weight of 0.4 is assigned to positive interactions, while a weight of 0.6 is assigned to negative interactions
                //The higher weight for negative interactions reflects their more destructive impact, emphasizing the importance of discouraging such behavior among trainers
                historical = (_scale * _overallPositiveHistory[_taskPublisher][_trainers[j]] * 4) / (_overallPositiveHistory[_taskPublisher][_trainers[j]] * 4 + _overallNegativeHistory[_taskPublisher][_trainers[j]] * 6);
                uint a = uncertaintyBetweenTrainerAndPublisher(_taskPublisher, _trainers[j], _taskId);
                // A weight of 0.5 is assigned to represent the impact of uncertainty in the interactions between the trainer and the publisher. This weight can be adjusted to control the influence of uncertainty
                _uncertainty_weight = 5;
                _subjectiveRep = historical * (_scale - a) + (a * _uncertainty_weight * _scale) / 10;
                // A weight of 0.8 is assigned to represent the impact of objective reputation, while a weight of 0.2 represents the effect of subjective reputation. These weights can be adjusted to control the influence of each reputation metric.
                // Assigning a higher weight to objective reputation is essential, as it reflects the trainer's performance in the current task. In contrast, subjective reputation is based on historical performance with a publisher.
                _weight_local_rep = 8;
                // we get the local reputation for the current time slot
                _localRep = ((10 - _weight_local_rep) * _subjectiveRep + (_weight_local_rep) * _objectiveRep) / 10;
            } else {
                // If it is the trainer's first interaction with a publisher, it indicates that the trainer has no existing subjective reputation
                _localRep = _objectiveRep;
            }
            // get the previous reputation
            _prevRep = taskContractInstance.getReputation(_trainers[j]);
            // The weights assigned during the reputation update are based on the total interactions of the trainer within the system. As the number of interactions increases, it becomes more challenging to raise the trainer's reputation score.
            _weight = uint256(calculateTanhLambdaX((int256(taskContractInstance.totalParticipationLevel(_trainers[j])) / 2 + 55) * 10000000));
            // If the trainer's behavior is judged positively, a higher weight is assigned to their previous reputation.
            // This emphasizes that the reputation score increases gradually, reflecting the consistent hard work and dedication of the trainer
            if (_scores[j] >= _goodBehaviourThreshold && _totalRounds[_taskId][_trainers[j]][_finishingRound] >= 2) {
                _newRep = (_weight * _prevRep + _localRep * (_scale - _weight));
            } 
            // If the trainer's behavior is judged negatively, a higher weight is assigned to their local reputation.
            // This highlights that the reputation score decreases significantly due to poor behavior, reflecting a strict policy aimed at discouraging such actions.
            else {
                _newRep = ((_scale - _weight) * _prevRep + _localRep * _weight);
            }
            // updating the reputation score of each trainer
            taskContractInstance.setReputation(_trainers[j], _newRep);
            // At the end of the task, store all positive and negative interactions to include them in the historical interaction records
            if (_finishingRound == _taskDetails.maxRounds) {
                _overallPositiveHistory[_taskPublisher][_trainers[j]] += _taskId * iterateMappingPositive(_taskDetails, _trainers[j]);
                _overallNegativeHistory[_taskPublisher][_trainers[j]] += _taskId * iterateMappingNegative(_taskDetails, _trainers[j]);
            }
        }
    }
}
