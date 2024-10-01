// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/shared/access/ConfirmedOwner.sol";
import "../system-contracts/businessLogic.sol";

/**
 * Request testnet LINK and ETH here: https://faucets.chain.link/
 * Find information on LINK Token Contracts and get the latest ETH and LINK faucets here: https://docs.chain.link/docs/link-token-contracts/
 */

/**
 * THIS IS AN EXAMPLE CONTRACT WHICH USES HARDCODED VALUES FOR CLARITY.
 * THIS EXAMPLE USES UN-AUDITED CODE.
 * DO NOT USE THIS CODE IN PRODUCTION.
 */

contract APIConsumer is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    BusinessLogic public businessContractInstance;

    uint256[] public volume;
    uint256[] public preRep;
    string public trainers;
    uint256[] public behaviour;
    string public globalModelWeightsHash;
    bytes32 private jobId;
    bytes32 private jobIdAggregator;
    bytes32 private jobIdPreRep;
    uint256 private fee;

    event RequestVolume(bytes32 indexed requestId, uint256[] volume);
    event RequestBehaviour(bytes32 indexed requestId, uint256[] behaviour);
    event RequestPreRep(bytes32 indexed requestId, uint256[] preRep);

    event RequestTrainers(bytes32 indexed requestId, string trainers);

    event RequestGlobalModelWeightsHash(
        bytes32 indexed requestId,
        string volume
    );

    /**
     * @notice Initialize the link token and target oracle
     *
     * Sepolia Testnet details:
     * Link Token: 0x779877A7B0D9E8603169DdbD7836e478b4624789
     * Oracle: 0x6090149792dAAeE9D1D568c9f9a6F6B46AA29eFD (Chainlink DevRel)
     * jobId: ca98366cc7314957b8c012c72f05aeeb
     *
     */
    constructor(
        address _linkContract,
        address _oracleContract
    ) ConfirmedOwner(msg.sender) {
        _setChainlinkToken(_linkContract);
        _setChainlinkOracle(_oracleContract);
        jobId = "6868419d5f6b42a7b5718abfb0c4c6c8";
        jobIdAggregator = "4545689b4d0d4d23917fcdbc5127328c";
        jobIdPreRep = "332cd9122a434ac7a2ac2514c835dd19";
        fee = (1 * LINK_DIVISIBILITY) / 10; // 0,1 * 10**18 (Varies by network and job)
    }

    // Set Business contract after both contracts are deployed
    function setBusinessContract(address _businessContract) external {
        businessContractInstance = BusinessLogic(_businessContract);
    }

    /**
     * Create a Chainlink request to retrieve API response, find the target
     * data, then multiply by 1000000000000000000 (to remove decimal places from data).
     */
    function requestVolumeData(
        string memory local_hash,
        string memory trainers,
        string memory model_hash,
        string memory global_weights_hash,
        string memory evaluation,
        string memory _round
    ) public returns (bytes32 requestId) {
        Chainlink.Request memory req = _buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfill.selector
        );
        volume = new uint256[](0);
        behaviour = new uint256[](0);
        // Set the URL to perform the GET request on
        req._add("local_hash", local_hash);
        req._add("trainers", trainers);
        req._add("model_hash", model_hash);
        req._add("global_weights_hash", global_weights_hash);
        req._add("evaluation", evaluation);
        req._add("round", _round);

        // Sends the request
        return _sendChainlinkRequest(req, fee);
    }

    function requestPreRepData(
        string memory trainers,
        string memory accuracies
    ) public returns (bytes32 requestId) {
        Chainlink.Request memory req = _buildChainlinkRequest(
            jobIdPreRep,
            address(this),
            this.fulfillRep.selector
        );
        preRep = new uint256[](0);
        // Set the URL to perform the GET request on
        req._add("trainers", trainers);
        req._add("accuracies", accuracies);

        // Sends the request
        return _sendChainlinkRequest(req, fee);
    }

    // call when aggregating
    function requestAggregation(
        string memory local_models,
        string memory scores,
        string memory model_hash
    ) public returns (bytes32 requestId) {
        Chainlink.Request memory req = _buildChainlinkRequest(
            jobIdAggregator,
            address(this),
            this.fulfillAggregation.selector
        );
        globalModelWeightsHash = "";

        // Set the URL to perform the GET request on
        req._add("local_models", local_models);
        req._add("scores", scores);
        req._add("global_model_hash", model_hash);

        // Sends the request
        return _sendChainlinkRequest(req, fee);
    }

    /**
     * Receive the response in the form of string
     */
    function fulfill(
        bytes32 _requestId,
        uint256[] memory _volume,
        uint256[] memory _behaviour
    ) public recordChainlinkFulfillment(_requestId) {
        emit RequestVolume(_requestId, _volume);
        emit RequestBehaviour(_requestId, _behaviour);
        volume = _volume;
        behaviour = _behaviour;
        // BusinessLogic.Score[] memory c = new BusinessLogic.Score[](_volume.length);
        // for (uint256 i = 0; i < _volume.length; i++) {
        //     c[i] = BusinessLogic.Score(_trainers[i], _volume[i], 111, 1);
        // }
        // businessContractInstance.submitScore(1,0,c);
    }

    function fulfillRep(
        bytes32 _requestId,
        uint256[] memory _volume,
        string memory _trainers
    ) public recordChainlinkFulfillment(_requestId) {
        emit RequestPreRep(_requestId, _volume);
        emit RequestTrainers(_requestId, _trainers);
        preRep = _volume;
        trainers = _trainers;
    }

    /**
     * Receive the response in the form of string
     */
    function fulfillAggregation(
        bytes32 _requestId,
        string memory _volume
    ) public recordChainlinkFulfillment(_requestId) {
        emit RequestGlobalModelWeightsHash(_requestId, _volume);
        globalModelWeightsHash = _volume;
    }

    /**
     * Allow withdraw of Link tokens from the contract
     */
    function withdrawLink() public onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(_chainlinkTokenAddress());
        require(
            link.transfer(msg.sender, link.balanceOf(address(this))),
            "Unable to transfer"
        );
    }

    function getVolume() public view returns (uint256[] memory) {
        return volume;
    }

    function getPreRep() public view returns (uint256[] memory) {
        return preRep;
    }

    function getTrainers() public view returns (string memory) {
        return trainers;
    }

    function getBehaviour() public view returns (uint256[] memory) {
        return behaviour;
    }
    function getGlobalModelWeightsHash() public view returns (string memory) {
        return globalModelWeightsHash;
    }
}
