from flask import Flask, request, jsonify
import ipfshttpclient
import json
import asyncio
import ast
import torch.nn as nn
import numpy as np
import random
from ipfs_model import IpfsModelLoader
from ipfs_weights import IpfsWeightsLoader
from FederatedLearning.utilities import load_data
from FederatedLearning import aggregation_algorithms
from FederatedLearning import aggregation
from FederatedLearning import ModelLoaders
from num import *
import torch



app = Flask(__name__)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/', methods=['POST'])
def call_adapter_sync():
    return asyncio.run(call_adapter_async())

@app.route('/aggregation', methods=['POST'])
def call_adapter_sync_aggregation():
    return asyncio.run(call_adapter_async_aggregation())


@app.route('/preReputation', methods=['POST'])
def call_adapter_sync_preRep():
    return asyncio.run(call_adapter_async_preRep())


## this function evaluates the local models every training round and assign scores to them
async def call_adapter_async(): 
    # getting the request body
    data = request.get_data()    
    data = json.loads(data)
    local_models_hashes=data["data"]["local_hash"]
    trainers=data["data"]["trainers"]
    global_model_hash=data["data"]["model_hash"]
    evaluation_method=data["data"]["evaluation"]
    round=data["data"]["round"]
    ## the validation dataset published by the task requester 
    validation_loader = load_data("party_0.npz")  
    criterion = nn.CrossEntropyLoss()
    # weights and model loaders from ipfs
    weights_loader = IpfsWeightsLoader()
    model_loader = IpfsModelLoader(weights_loader)
    # here is the global model weights
    model = model_loader.load(global_model_hash) 
    # getting the trainers addresses
    trainers = trainers.split("-")
    # getting the local models weights
    local_cid = local_models_hashes.split("-")
    all_weights = []
    # accessing every trainer'slocal model
    for i,c in enumerate(local_cid):    
        weights = get_model_weights(c)
        weights = weights.decode()    
        weights = np.array(ast.literal_eval(weights))
        all_weights.append(weights)
    scores = []    
    if evaluation_method == "similarity":
        scores = weights_similarity_based_evaluation(trainers,all_weights,global_model_hash) 
    elif evaluation_method == "accuracy":
        scores  = accuracy_based(all_weights, model , validation_loader, criterion)
    ## the response returned to the oracle operator 
    eaResponse = {"data": {"scores": scores},
                  "jobRunId": data["id"]
                  }
    try:
        return jsonify(eaResponse)
    except exceptions.ErrorResponse as error:
    # Handle the error
        print(f"Error: {error}")
  

## this function aggregates the local models into a global model
async def call_adapter_async_aggregation():
    # getting the request body
    data = request.get_json(force=True)
    #local_models_hashes=data["data"]["number"]
    local_models_hashes=data["data"]["local_models"]
    scores=data["data"]["scores"]
    global_model_hash=data["data"]["global_model_hash"]
    global_weights_hash=data["data"]["global_weights_hash"]
    round=data["data"]["round"]
    trainers=data["data"]["trainers"]
    # weights and model loaders from ipfs
    weights_loader = IpfsWeightsLoader()
    model_loader = IpfsModelLoader(weights_loader)
    # getting the global model
    model = model_loader.load(global_model_hash) 

    # getting the trainers scores returned of the training round
    scores = scores.split("-")
    # here is the local models weights
    local_cid = local_models_hashes.split("-")
     # getting the trainers addresses
    trainers = trainers.split("-")
    all_weights = []
    # accessing every trainer'slocal model
    for c in local_cid:
        weights = get_model_weights(c)
        weights = np.array(ast.literal_eval(weights.decode()))
        all_weights.append(weights.tolist())

    score_index = 0
    for element in scores:
        scores[score_index] = int(element)
        score_index+=1
    # aggregation method -fedAvg
    fed_avg_aggregator = aggregation_algorithms.FedAvgAggregator(ModelLoaders.Model(model).count, weights_loader)
    _aggregator = aggregation.Aggregator(weights_loader,fed_avg_aggregator)
    weights_cid  = _aggregator.aggregate(all_weights,scores)
    validation_loader = load_data("party_0.npz")
    criterion = nn.CrossEntropyLoss()
    # set the aggregated weights as the global model weights and calculate the accuracy
    model = model_loader.load(global_model_hash,weights_cid) 
    gm_accuracy = calculate_accuracy(model , validation_loader, criterion)    
    # turn accuracy to int because solidity does not allow float and decimals
    gm_accuracy = float_to_int(gm_accuracy)
    # return the global model's weight along with its accuracy to the oracles operator    
    eaResponse = {"data": {"globalModelWeightsHash": weights_cid,
                           "globalModelWeightsAccuracy": gm_accuracy
                            },
                  "jobRunId": data["id"]
                  }
    try:
        return jsonify(eaResponse)
    except exceptions.ErrorResponse as error:
    # Handle the error
        print(f"Error: {error}")
  



async def call_adapter_async_preRep():
    # getting the request body
    data = request.get_json(force=True)
    trainers=data["data"]["trainers"]
    accuracies=data["data"]["accuracies"]
    weights_loader = IpfsWeightsLoader()
    model_loader = IpfsModelLoader(weights_loader)
    # getting the trainers addresses
    trainers = trainers.split("-")
    accuracies = accuracies.split("-")
    # sort the trainers models accuracies
    sorted_trainers ,  sorted_acc   = sort_scores(accuracies,trainers)
    sorted_trainers = '-'.join(sorted_trainers)
    eaResponse = {"data": {"scores": sorted_acc ,
                           "addrs": sorted_trainers },
                  "jobRunId": data["id"]
                  }
    try:
        return jsonify(eaResponse)
    except exceptions.ErrorResponse as error:
    # Handle the error
        print(f"Error: {error}")
  

def sort_scores(values , labels):
    # Combine both arrays into a list of tuples
    combined = list(zip(values, labels))

    # Sort the combined list by the first element (values) in descending order
    sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # Unzip the sorted list back into two separate lists
    sorted_values, sorted_labels = zip(*sorted_combined)

    # Convert back to lists (if needed)
    sorted_values = list(sorted_values)
    sorted_labels = list(sorted_labels)
    return sorted_labels , sorted_values 




def accuracy_based(submissions, model , test_dataloader, criterion):
    scores = []
    for i, submission in enumerate(submissions):
        if len(submission)>0:
            model.set_weights(model,submission)
            local_model_accuracy = calculate_accuracy(model , test_dataloader, criterion)
            scores.append(local_model_accuracy) 
        else:
            scores.append(0)
    converted_adjusted_normalized_scores = [float_to_int(value,1e18) for value in scores]
    return converted_adjusted_normalized_scores 



def calculate_accuracy(model , test_dataloader, criterion):
    model.eval()  # Set the model to evaluation mode
    total_loss = 0.0
    correct_predictions = 0
    total_samples = 0
    with torch.no_grad():  # Disable gradient computation
        for inputs, labels in test_dataloader:
        #inputs, labels = inputs.to(device), labels.to(device)  # Move data to the same device as the model
            outputs = model(inputs)  # Get model predictions
            loss = criterion(outputs, labels)  # Calculate loss
            total_loss += loss.item()  # Aggregate loss
            _, predicted = torch.max(outputs, 1)  # Get the predicted class
            correct_predictions += (predicted == labels).sum().item()  # Count correct predictions
            total_samples += labels.size(0)  # Count total samples
    # Calculate average loss and accuracy
    average_loss = total_loss / len(test_dataloader)
    accuracy = correct_predictions / total_samples
    return accuracy


def similarity_with_global_model(weights_trainer,weights_previous_gm):
    max_len = max(len(weights_trainer), len(weights_previous_gm))
    padded_i = [float(x) for x in weights_trainer] + [0] * (max_len - len(weights_trainer))
    padded_j = [float(x) for x in weights_previous_gm] + [0] * (max_len - len(weights_previous_gm))
    distance =    sum(
            (padded_j[k] - padded_i[k]) ** 2
            for k in range(max_len)
        ) ** 0.5
    return distance


# weights similarity based evaluation
def weights_similarity_based_evaluation(trainers,all_weights,global_model_hash):
    r = len(all_weights)
    f = int(r / 3) - 1
    closest_updates = r - f - 2
    similarities = []
    for i in range(len(all_weights)):
        dists = []
        for j in range(len(all_weights)):
            if i == j:
                continue
            if i != j:
                max_len = max(len(all_weights[i]), len(all_weights[j]))
                padded_i = [float(x) for x in all_weights[i]] + [0] * (max_len - len(all_weights[i]))
                padded_j = [float(x) for x in all_weights[j]] + [0] * (max_len - len(all_weights[j]))
                dists.append(
                    sum(
                        (padded_j[k] - padded_i[k]) ** 2
                        for k in range(max_len)
                    ) ** 0.5
                )
        dists_sorted = sorted(range(len(dists)), key=lambda x: dists[x])[:closest_updates]
        similarity = sum(dists[idx] for idx in dists_sorted)  
        similarities.append(similarity)
    weights_loader = IpfsWeightsLoader()
    model_loader = IpfsModelLoader(weights_loader)
    model = model_loader.load(global_model_hash) 
    fed_avg_aggregator = aggregation_algorithms.FedAvgAggregator(ModelLoaders.Model(model).count, weights_loader)
    adjusted_normalized_scores = fed_avg_aggregator.calculate_adjusted_min_max_normalized_scores(similarities)
    converted_adjusted_normalized_scores = [float_to_int(value) for value in adjusted_normalized_scores]
    return converted_adjusted_normalized_scores



# gets smth stored on ipfs using its hash
def get_model_weights(hash):
    client = ipfshttpclient.connect('/ip4/0.0.0.0/tcp/5001')
    stream = client.cat(hash)
    return stream


## generate random model weights
def perturb_array(original_array, perturbation_factor):
    perturbed_array = []
    for weight in original_array:
        perturbation = random.uniform(-perturbation_factor, perturbation_factor)
        new_weight =  perturbation
        perturbed_array.append(new_weight)
    return perturbed_array

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8089', threaded=True)
