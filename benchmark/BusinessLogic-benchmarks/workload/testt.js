'use strict';
const fs = require('fs');
const { WorkloadModuleBase } = require('@hyperledger/caliper-core');
const Web3 = require('web3');
var listTasks = [];
var isInit = false;



class StoreWorkload extends WorkloadModuleBase {

    /**
     * Initializes the parameters of the workload.
     */
    constructor() {
        super();
        this.txIndex = -1;
        this.private = false;
        this.contract = {};
    }  

    

    /**
     * Generates simple workload.
     * @returns {{verb: String, args: Object[]}[]} Array of workload argument objects.
     */
    _generateWorkload() {
        let web3 = new Web3(this.nodeUrl);
    /** Read inputs for the workload config from files */
        let workload = [];
        if(!isInit){
            isInit = true;
            // publishTask setup
            // You can use .json instead since you have multiple params 
          const allFileContents = fs.readFileSync("./workload/workload.json");
          var data= JSON.parse(allFileContents);
          console.log(data)
          data.split(/\r?\n/).forEach(line =>  {  
            // Here you push a json object 
            listTasks.push(line);
           // console.log(${line});
            });
 
      }

      console.log("here   ",listTasks[0])
       // MUST -> this.roundArguments.txnPerBatch < listTasks.length
        
        for(let i= 0; i < this.roundArguments.txnPerBatch; i++) {
            this.txIndex++;
          
        // init args for publishTask   
        var args;
        // use the first 3000 params
        if(this.roundArguments.num==1){
             args = {
                contract: this.roundArguments.contract,
                verb: 'publishTask',
                args: [listTasks[this.txIndex]],
                readOnly: false,
            }
        } 
        // use params from 3000 -> 6000
        else if(this.roundArguments.num==2){
            args = {
                contract: this.roundArguments.contract,
                verb: 'publishTask',
                args: [listTasks[this.txIndex+200]],
                readOnly: false,
            }
        }
       // use params from 400 -> 600
        // else{
        //     args = {
        //         contract: this.roundArguments.contract,
        //         verb: 'publishTask',
        //         args: [listTasks[this.txIndex+400]],
        //         readOnly: false,
        //     }
        // }
            if (this.isPrivate) {
                args.privacy = this.privclacyOpts;
                args.privacy.sender = web3.eth.accounts.create();
                args.privacy.sender.nonce = 0;
            }

            workload.push(args);
        }

        return workload;
    }

    /**
     * Initialize the workload module with the given parameters.
     * @param {number} workerIndex The 0-based index of the worker instantiating the workload module.
     * @param {number} totalWorkers The total number of workers participating in the round.
     * @param {number} roundIndex The 0-based index of the currently executing round.
     * @param {Object} roundArguments The user-provided arguments for the round from the benchmark configuration file.
     * @param {BlockchainConnector} sutAdapter The adapter of the underlying SUT.
     * @param {Object} sutContext The custom context object provided by the SUT adapter.
     * @async
     */
    async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

        if (!this.roundArguments.contract) {
            throw new Error('store - argument "contract" missing');
        }

        this.nodeUrl = sutContext.url;

        if(this.roundArguments.private) {
            this.isPrivate = true;
            this.privacyOpts = sutContext.privacy[this.roundArguments.private];
            this.privacyOpts['id'] = this.roundArguments.private;
        } else {
            this.isPrivate = false;
        }

        if(!this.roundArguments.txnPerBatch) {
            this.roundArguments.txnPerBatch = 1;
        }
    }

    /**
     * Assemble TXs for opening new accounts.
     */
    async submitTransaction() {
        let args = this._generateWorkload();
      //  console.log(args);
        await this.sutAdapter.sendRequests(args);
    }

    
}

  

function createWorkloadModule() {
    return new StoreWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
