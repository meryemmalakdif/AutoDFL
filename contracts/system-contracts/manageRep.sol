// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./businessLogic.sol";
import "./SafeMath.sol" ;
import "./Math.sol" ;
import "./FixedPointMath.sol" ;


// for now this is to calculate the objective automated reputation  aka evaluate a trainer's work in the current task => deterministic reputation
contract ManageReputation {


    // imported libraries 
    // using SafeMath for uint256;
    // using Math for *; 
    using FixedPointMath for int256;


    // events
    event performanceMeasured(uint256,uint256);
    event scoresFetched(int256[]);  
    event scoreTrainerFetched(int256); 
    event recencyGot(uint256);
    event interactionsTP(uint256,uint256);

    // Calculation



    //uint _scale = 10**17; 
    uint _scale = 1000000 ;
    uint256 _scaleScore = 1e18 ; // 1000000000000000000
    uint256 _scaling= 1e14 ;
    uint256 _scaleDifference = _scaleScore/_scale ;


    // Imported contracts
    BusinessLogic public  taskContractInstance ;
    mapping(address => mapping(address => uint256)) public _overallPositiveHistory;   // address TP => address trainer => value
    mapping(address => mapping(address => uint256)) public _overallNegativeHistory;   // address TP => address trainer => value
    
    
    mapping(uint => mapping(address => mapping(uint => uint256))) public _roundPositivePerformance;   // task id => trainer => round => + performance
    mapping(uint => mapping(address => mapping(uint => uint256))) public _roundNegativePerformance;   // task id => trainer => round => - performance

    mapping(uint => mapping(address => mapping(uint => uint256))) public _totalRounds;   // task id => trainer => round => + performance

    constructor(address _taskContractAddress){
        taskContractInstance = BusinessLogic(_taskContractAddress);
    }
   

    function calculateTanhLambdaX(int256 x) public pure returns (int256) {
        return x.tanhLambdaX();
    }
   
    // it is based on the historical interactions between a task publisher and a trainer 
    // when we 
    function automatedReputation(address _taskPublisher , address _trainer , uint taskId) public returns(uint256)
     {
        uint256 _result = 0;
        uint256 _u ;

       uint256 _interactionsTpTa = taskContractInstance.historicalInteractions(_taskPublisher , _trainer , taskId) ;
       uint256 _interactionsTp = 0 ;

       address[] memory _allTrainers = taskContractInstance.getAllTrainers() ;
        for (uint j = 0 ; j < _allTrainers.length ; j++)
           {
            _interactionsTp += taskContractInstance.interactionTaskPublisherTrainer(_taskPublisher , _allTrainers[j]) ;
           }
        // balanced uncertainty , have not found anything that can help me determine its right value so 0.5
        uint256 _uncertainty = 5;   
        if(_interactionsTp>0){
         _u = _scale-(_interactionsTpTa*_scale / _interactionsTp) ; //   6        
        }
           return _u ;  
     }

        function iterateMappingPositive(BusinessLogic.Task memory _taskDetails , address _addr) public view returns (uint256) {
            uint256 _result = 0;
            for (uint i = 0; i < _taskDetails.maxRounds; i++) {
                _result+= _roundPositivePerformance[_taskDetails.taskId][_addr][i+2];
            }
            return _result ; 
        }

        function iterateMappingNegative(BusinessLogic.Task memory _taskDetails , address _addr) public view returns (uint256) {
            uint256 _result = 0;
            for (uint i = 0; i < _taskDetails.maxRounds; i++) {
                _result+= _roundNegativePerformance[_taskDetails.taskId][_addr][i+2];
            }
            return _result ; 
        }


   

function abs(int256 x) private pure returns (uint256) {
    return x >= 0 ? uint256(x) : uint256(-x);
}


    // u need to figure out what s the best way to calculate the weight here
    function updateRepuation(uint _taskId,uint _startingRound , uint _finishingRound , address[] memory _trainers , uint256[] memory _scores , uint256[] memory totalRounds) public  {

        uint historical = 0 ;
        BusinessLogic.Task memory _taskDetails = taskContractInstance.getTaskById(_taskId);
        address _taskPublisher = _taskDetails.publisher ; 
        uint256 _prevRep = 0 ;
        uint256 _newRep = 0 ;
        uint256 _localRep ;
        uint _threshold =  _trainers.length*2/3 ;
        uint256 _weight ;
        uint256 _weight_local ;
        uint256 _subjectiveRep ;
        uint256 _goodBehaviourThreshold = 0 ;

        for (uint j = 0 ;   j <= _threshold-1; j++){
            _goodBehaviourThreshold = _goodBehaviourThreshold + _scores[j];
        }
        _goodBehaviourThreshold = _goodBehaviourThreshold / _threshold ;

        uint256 _givenScore  ;

        for (uint j = 0; j < _trainers.length; j++)
        {
            _givenScore = 0 ;
            // update for the coming rounds and tasks 
            if ((_scores[j]+150000000000000000)>=_goodBehaviourThreshold){
                // good behaviour in time slot
                _roundPositivePerformance[_taskId][_trainers[j]][_finishingRound] += _scores[j]*_finishingRound ; // 19
                 _givenScore = _scale*_scale*totalRounds[j]/4;

            }  
            else{
                _roundNegativePerformance[_taskId][_trainers[j]][_finishingRound] += _scores[j]*_finishingRound ;
                _givenScore = 4*_scale*_scale*totalRounds[j]/40 ;

            } 







                

            // calculate subjective rep
            if(taskContractInstance.totalNumberOfTasksWithPublisher(_trainers[j], _taskDetails.publisher)>1)
            {
                historical = (_scale*_overallPositiveHistory[_taskPublisher][_trainers[j]] * 4)/(_overallPositiveHistory[_taskPublisher][_trainers[j]]*4+_overallNegativeHistory[_taskPublisher][_trainers[j]]*6); // _scale
                uint a = automatedReputation(_taskPublisher,_trainers[j], _taskId); // _scale
                _subjectiveRep = historical*(_scale-a)+a*5*_scale/10;  // _scale * _scale 
                _weight_local = 8 ;
                _localRep = ((10-_weight_local)*_subjectiveRep + (_weight_local)*_givenScore)/10 ; // _scale ** 2  
                

            }
            else {
                _localRep = _givenScore ; 
            } 

                _prevRep = taskContractInstance.getReputation(_trainers[j]);
            _weight = uint256(calculateTanhLambdaX((int256(taskContractInstance.totalParticipationLevel(_trainers[j]))/2+55)*10000000)) ;  // 6 was 96 was 116 last time
             if (_scores[j] >=_goodBehaviourThreshold && _totalRounds[_taskId][_trainers[j]][_finishingRound]>=2)
            {            
                _newRep = (_weight*_prevRep + _localRep*(_scale-_weight)); // more weight will be assigned to the oldRep
            }
            else
            { 
                _newRep = ((_scale-_weight)*_prevRep + _localRep*_weight); // more weight will be assigned to the local rep
            }  
            taskContractInstance.setReputation(_trainers[j],_localRep); 
            
               


                if(_finishingRound == _taskDetails.maxRounds)
        {        
            //_weight = calculateTanhLambdaX(int256(taskContractInstance.totalNumberOfTasksWithPublisher(_trainer[j], _taskPublisher)+56)*10000000);    //*  this part am not sure how to do it       int256(_taskParticipationLevel) ;
            _overallPositiveHistory[_taskPublisher][_trainers[j]] += _taskId*iterateMappingPositive(_taskDetails,_trainers[j]);  // 
            _overallNegativeHistory[_taskPublisher][_trainers[j]] += _taskId*iterateMappingNegative(_taskDetails,_trainers[j]);  // 31
        }        
        }
    }


  


}

