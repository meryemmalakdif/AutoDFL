// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


contract AccesManagement {
    
    address private admin;
    address  [] public adminsList ; 
    mapping(address => bool) public adminExist;
 

    address[] public _taskPublishers;
    address[] public _trainers;    

    address [] private oracleAdresses; 
    mapping (address => bool) private oracleExist ; 

    constructor() {
        admin = msg.sender;
        adminsList.push(admin); 
        adminExist[admin]= true;
    }

    modifier onlyOwner() {
        require(adminExist[msg.sender] == true, "Only the contract owner can call this function.");
        _;
    }

    modifier onlyOracle() {
        require(oracleExist[msg.sender] == true, "Only the oracle can call this function.");
        _;
    }

    function addOwner(address _newOwner) public onlyOwner {
        adminsList.push(_newOwner); 
        adminExist[_newOwner]= true;
    }

    function addOracleAdress(address _address) public onlyOwner(){
        oracleAdresses.push(_address);
        oracleExist[_address]=true;
    }
    

    function isOwner(address _user) public view returns (bool) {
        return adminExist[_user];
    }
    
    function isTrainer(address _addr) public view returns  (bool){
        bool found = false;
        if (_trainers.length > 0) {
            for (uint i = 0; i < _trainers.length; i++) {
                if (_trainers[i] == _addr) {
                    found = true;
                    break;
                }
            }
        }
        return found;
    }


    function isTaskPublisher(address _addr) public view returns  (bool){
        bool found = false;
        if (_taskPublishers.length > 0) {
            for (uint i = 0; i < _taskPublishers.length; i++) {
                if (_taskPublishers[i] == _addr) {
                    found = true;
                    break;
                }
            }
        }
        return found;
    }    

    function isOracle(address _address)public view returns (bool){
        return oracleExist[_address];
    }
}

