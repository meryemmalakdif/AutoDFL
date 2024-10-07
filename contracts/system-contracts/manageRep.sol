// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./businessLogic.sol";
import "./libraries/FixedPointMath.sol";

contract ManageReputation {
    // imported libraries
    using FixedPointMath for int256;

    // Imported contracts
    BusinessLogic public taskContractInstance;

    // uint _scale = 10**17;
    uint _scale = 1000000;
    uint256 _scaleScore = 1e18; // 1000000000000000000
    uint256 _scaling = 1e14;
    uint256 _scaleDifference = _scaleScore / _scale;

    mapping(address => mapping(address => uint256)) public _overallPositiveHistory; // address TP => address trainer => value
    mapping(address => mapping(address => uint256)) public _overallNegativeHistory; // address TP => address trainer => value

    constructor(address _taskContractAddress) {
        taskContractInstance = BusinessLogic(_taskContractAddress);
    }

    function calculateTanhLambdaX(int256 x) public pure returns (int256) { 
        return x.tanhLambdaX(); 
    }

    // Reputation updates occur at the end of each timeslot, which is composed of multiple training rounds
    function calculateObjectiveReputation(uint _taskId, address[] memory _trainers, uint256[] memory _scores, uint256[] memory totalRounds) public returns (uint256[] memory, uint256) {
        BusinessLogic.Task memory _taskDetails = taskContractInstance.getTaskById(_taskId);
        address _taskPublisher = _taskDetails.publisher;
        uint _threshold = (_trainers.length * 2) / 3;
        uint256 _goodBehaviourThreshold = 0;
        uint256 _tolerableRange;
        
        // get the threshold for good behaviour
        for (uint j = 0; j <= _threshold - 1; j++) {
            _goodBehaviourThreshold += _scores[j];
        }
        _goodBehaviourThreshold /= _threshold;

        uint256[] memory _objectiveRep = new uint256[](_trainers.length);

        for (uint j = 0; j < _trainers.length; j++) {
            // check whether a trainer has good or bad behaviour with a tolerable range
            if ((_scores[j] + _tolerableRange) >= _goodBehaviourThreshold && totalRounds[j] >= (_taskDetails.maxRounds/2) ) {
                _overallPositiveHistory[_taskPublisher][_trainers[j]] += _scores[j] * _taskId;
                // the obj rep considers the number of the completed rounds 
                _objectiveRep[j] = (_scale * _scale * totalRounds[j]) / _taskDetails.maxRounds;
            } else {
                _overallNegativeHistory[_taskPublisher][_trainers[j]] += _scores[j] * _taskId;
                _objectiveRep[j] = (4 * _scale * _scale * totalRounds[j]) / (_taskDetails.maxRounds*10);
            }
        }
        return (_objectiveRep, _goodBehaviourThreshold);
    }

    // Reputation updates occur at the end of each timeslot, which is composed of multiple training rounds
    function calculateSubjectiveReputation(uint _taskId, address _trainer) public returns (uint256) {
        BusinessLogic.Task memory _taskDetails = taskContractInstance.getTaskById(_taskId);
        address _taskPublisher = _taskDetails.publisher;
        uint256 historical;
        // A weight of 0.5 is assigned to represent the impact of uncertainty in the interactions between the trainer and the publisher. This weight can be adjusted to control the influence of uncertainty
        uint256 _uncertainty_weight = 5;
        uint256 _subjectiveRep ;
        uint256 _u;
        // all the interactions a publisher has with all the system's trainers excluding the current task
        uint256 _interactionsTp = taskContractInstance.publisherTotalInteractions(_taskPublisher) - _taskDetails.trainers.length;  // the minus is to exclude the current task from the count because the subjective rep only considers historical interactions    
        // all interactions of a trainer with a publisher excluding the current task 
        uint256 _interactionsTpTa = taskContractInstance.historicalInteractions(_taskPublisher, _trainer) - 1;
        // measure the belief a publisher has in a trainer
        if (_interactionsTp > 0) {
            _u = _scale - ((_interactionsTpTa * _scale) / _interactionsTp); 
        }
        historical = (_scale * _overallPositiveHistory[_taskPublisher][_trainer] * 4) / (_overallPositiveHistory[_taskPublisher][_trainer] * 4 + _overallNegativeHistory[_taskPublisher][_trainer] * 6);
        _subjectiveRep = historical * (_scale - _u) + (_u * _uncertainty_weight * _scale) / 10;
        return _subjectiveRep;
    }

    // Reputation update occurs at the end of each task
    function updateReputation(uint _taskId, address[] memory _trainers, uint256[] memory _scores, uint256[] memory totalRounds) public {
        BusinessLogic.Task memory _taskDetails = taskContractInstance.getTaskById(_taskId);
        uint256 _prevRep;
        uint256 _newRep;
        uint256 _localRep;
        uint256 _weight;
        uint256 _weight_local_rep;
        uint256 _subjectiveRep ;
     
        // objective reputation
        (uint256[] memory _objectiveRep, uint256 _goodBehaviourThreshold) = calculateObjectiveReputation(_taskId, _trainers, _scores, totalRounds);
  
        for (uint j = 0; j < _trainers.length; j++) {
            // Calculate subjective reputation
            if ((taskContractInstance.historicalInteractions(_taskDetails.publisher,_trainers[j]) -1) > 1) {
                // subjective reputation
                _subjectiveRep = calculateSubjectiveReputation(_taskId, _trainers[j]);
     
                // A weight of 0.8 is assigned to represent the impact of objective reputation, while a weight of 0.2 represents the effect of subjective reputation. These weights can be adjusted to control the influence of each reputation metric.
                // Assigning a higher weight to objective reputation is essential, as it reflects the trainer's performance in the current task. In contrast, subjective reputation is based on historical performance with a publisher.
                
                _weight_local_rep = 8;
                // we get the local reputation for the current time slot
                _localRep = ((10 - _weight_local_rep) * _subjectiveRep + (_weight_local_rep) * _objectiveRep[j]) / 10;
            } else {
                // If it is the trainer's first interaction with a publisher, it indicates that the trainer has no existing subjective reputation
                _localRep = _objectiveRep[j];
            }
            // get the previous reputation
            _prevRep = taskContractInstance.getReputation(_trainers[j]);
            // The weights assigned during the reputation update are based on the total interactions of the trainer within the system. As the number of interactions increases, it becomes more challenging to raise the trainer's reputation score.
            _weight = uint256(calculateTanhLambdaX((int256(taskContractInstance.totalNumberOfTasks(_trainers[j]))) * 10000000));
            // If the trainer's behavior is judged positively, a higher weight is assigned to their previous reputation.
            // This emphasizes that the reputation score increases gradually, reflecting the consistent hard work and dedication of the trainer
            if (_scores[j] >= _goodBehaviourThreshold && totalRounds[j] >= _taskDetails.maxRounds) {
                _newRep = (_weight * _prevRep + _localRep * (_scale - _weight));
            } 
            // If the trainer's behavior is judged negatively, a higher weight is assigned to their local reputation.
            // This highlights that the reputation score decreases significantly due to poor behavior, reflecting a strict policy aimed at discouraging such actions.
            else {
                _newRep = ((_scale - _weight) * _prevRep + _localRep * _weight);
            }
            // updating the reputation score of each trainer
            taskContractInstance.setReputation(_trainers[j], _newRep / _scale);
        }
    }

}
