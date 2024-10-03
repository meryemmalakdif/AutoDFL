from flask import Flask, request, jsonify
import ipfshttpclient
import json
import asyncio
import ast
import torch.nn as nn
from web3 import Web3
import numpy as np
import random
# from FederatedLearning import ModelLoaders
# from FederatedLearning import weights_loaders
from ipfs_model import IpfsModelLoader
from ipfs_weights import IpfsWeightsLoader
from FederatedLearning.utilities import load_data
from FederatedLearning import aggregation_algorithms
from FederatedLearning import aggregation
from FederatedLearning import ModelLoaders
from model import Model
from architecture import LeNet5
from num import *
from model import Model
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



# evaluate using the delete instance method
# we include a specific local model in the aggregated global model then we exclude it
# calculate the accuracy in both senarios then see the local model's impact
async def call_adapter_async():
    
    # getting the request body
    data = request.get_data()

    # data = request.get_json(force=True)
    
    data = json.loads(data)
    #local_models_hashes=data["data"]["number"]


    local_models_hashes=data["data"]["local_hash"]
    trainers=data["data"]["trainers"]
    global_model_hash=data["data"]["model_hash"]
    global_weights_hash=data["data"]["global_weights_hash"]
    evaluation_method=data["data"]["evaluation"]

    round=data["data"]["round"]



    validation_loader = load_data("party_0.npz")
    
    criterion = nn.CrossEntropyLoss()
    weights_loader = IpfsWeightsLoader()

    model_loader = IpfsModelLoader(weights_loader)
    # here is the global model weights
    model = model_loader.load(global_model_hash,global_weights_hash) 
    model1 = model_loader.load(global_model_hash) 


    # getting the trainers addresses
    trainers = trainers.split("-")

    # here is the local models weights
    local_cid = local_models_hashes.split("-")

    if int(round)==0:
        previous_gm_weights = weights_loader.load("QmZ8buiBbQGSF2C8yTxNeJPBHc8GzNdDvbHVNgn8KX8M8f") 
    else:
        previous_gm_weights = weights_loader.load(global_weights_hash) 



 
    all_weights = []


    # for i,c in enumerate(local_cid):
    #     if (trainers[i]!="0xA13c10C0D5bd6f79041B9835c63f91de35A15883" and int(round)%2==0) or int(round)%2!=0:
    #         # simulate senarios of behaviours
    #         ## first senario a malicious trainer takes the previous global model's weights and slightly changes them 
    #         if int(round)!=0 and trainers[i] == "0x0D43eB5B8a47bA8900d84AA36656c92024e9772e":
    #             all_weights.append(np.array(perturb_array(previous_gm_weights, 25.3)))
    #         else:
    #             weights = get_model_weights(c)

    #         # weights = weights.decode()

    #         # print("Shape of weights_array:", type(weights))
    #         # # weights_array = pickle.loads(weights)
    #         # weights_list = eval(weights)

    #         # # Convert the list to a NumPy array
    #         # weights = np.array(weights_list)

    #         # # Now you can access the shape
    #         # print("Shape of weights:", weights.shape)

    #         # random_weights = np.random.randn(*weights.shape)

    #         # # Check for NaN values
    #         # if np.isnan(random_weights).any():
    #         #     print("Random weights contain NaN values!")
    #         # else:
    #         #     print("Random weights generated successfully.")
    #         # with open('mimi.txt', 'a') as f:
    #         #     f.write(f"papa : {random_weights}\n") 

    #         # print("Shape of weights_array:", weights.shape)

    #         # with open('mimi.txt', 'a') as f:
    #         #     f.write(f" {trainers[i]} : {weights.decode()}\n") 
    #             weights = weights.decode()            
    #             weights = np.array(ast.literal_eval(weights))

    #             all_weights.append(weights)
    #     else:
    #         if int(round)%2 == 0:
    #             all_weights.append([])



# normal senario where every trainer contributes honestly
    for i,c in enumerate(local_cid):
        
        weights = get_model_weights(c)
        weights = weights.decode()    
        weights = np.array(ast.literal_eval(weights))
        


        all_weights.append(weights)

    scores = []
    interaction_type = []

    
    trainers =[]
    if evaluation_method == "similarity":
        scores = weights_similarity_based_evaluation(trainers,all_weights,global_model_hash) 
    elif evaluation_method == "accuracy":
        scores , interaction_type  = accuracy_based(all_weights, model1 , validation_loader, criterion)


    

    eaResponse = {"data": {"scores": scores,
                           "trainers":trainers,
                           "behaviour":interaction_type
                           },
                  "jobRunId": data["id"]
                  }
    try:
        return jsonify(eaResponse)
    except exceptions.ErrorResponse as error:
    # Handle the error
        print(f"Error: {error}")
  

# evaluate using the delete instance method
# we include a specific local model in the aggregated global model then we exclude it
# calculate the accuracy in both senarios then see the local model's impact
async def call_adapter_async_aggregation():
    # getting the request body
    data = request.get_json(force=True)
    #local_models_hashes=data["data"]["number"]
    local_models_hashes=data["data"]["local_models"]
    scores=data["data"]["scores"]
    global_model_hash=data["data"]["global_model_hash"]
    global_weights_hash=data["data"]["global_weights_hash"]
    round=data["data"]["round"]


    weights_loader = IpfsWeightsLoader()
    model_loader = IpfsModelLoader(weights_loader)
    # getting the trainers addresses
    scores = scores.split("-")
    # here is the local models weights
    local_cid = local_models_hashes.split("-")
    all_weights = []
    previous_gm_weights = []
    if int(round)!=0:
        previous_gm_weights = weights_loader.load(global_weights_hash) 

    # for i,c in enumerate(local_cid):
    #     if (i==0 or i==2 ):
    #         if int(round)!=0:
    #             all_weights.append(np.array(random_model(previous_gm_weights)).tolist())
    #         else:
    #             all_weights.append(np.array([]).tolist())
    #     elif (i==1 or i==3 or i==5 or i==4):
    #         weights = get_model_weights(c)
    #         weights = weights.decode()            
    #         weights = np.array(ast.literal_eval(weights))

    #         all_weights.append(weights.tolist())
    #     else:
    #         if int(round)%2==0:
    #          all_weights.append(np.array([]).tolist())
    #         else:
    #             weights = get_model_weights(c)
    #             weights = weights.decode()            
    #             weights = np.array(ast.literal_eval(weights))

    #             all_weights.append(weights.tolist())    



# good behaviour
    for c in local_cid:
        weights = get_model_weights(c)
        weights = np.array(ast.literal_eval(weights.decode()))
        
        all_weights.append(weights.tolist())



    model = model_loader.load(global_model_hash) 
    score_index = 0
    for element in scores:
        scores[score_index] = int(element)
        score_index+=1

    # scores = [int(element) for element in scores]
    # aggregation method
    fed_avg_aggregator = aggregation_algorithms.FedAvgAggregator(ModelLoaders.Model(model).count, weights_loader)
    _aggregator = aggregation.Aggregator(weights_loader,fed_avg_aggregator)
    weights_cid  = _aggregator.aggregate(all_weights,scores)
    validation_loader = load_data("party_0.npz")
    
    criterion = nn.CrossEntropyLoss()

    model = model_loader.load(global_model_hash,weights_cid) 


    gm_accuracy = calculate_accuracy(model , validation_loader, criterion)    
    gm_accuracy = float_to_int(gm_accuracy)

    print("t9il ",gm_accuracy)
    
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

    sorted_trainers ,  sorted_acc   = sort_scores(accuracies,trainers)
    sorted_trainers = '-'.join(sorted_trainers)
    # sorted_acc = '-'.join(sorted_acc)

  
    
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



def calculate_weighted_average(data):
    weights = [0.1,0.2,0.3 ,0.4]  # Example weights that decrease
    weighted_averages = []
    
    for item in data:
        numbers = list(map(int, item.split('-')))
        weighted_sum = sum(num * weight for num, weight in zip(numbers, weights))
        total_weight = sum(weights)
        weighted_average = weighted_sum / total_weight
        weighted_averages.append(weighted_average)
    
    return weighted_averages



def aggregate(submissions,model_size):
    samples = [62,69,43]
    # the impact a specific model update has when aggregating is measured based on its data size
    
    # refactor ya bent
    return weighted_fed_avg(submissions, model_size, samples)

def validate(model , test_dataloader, criterion):
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
    return {'average_loss': average_loss, 'accuracy': accuracy}

def weighted_fed_avg(submissions, model_size, avg_weights):
  total_weights = np.sum(avg_weights)
  new_weights = np.zeros(model_size)

  for i, submission in enumerate(submissions):
    if submission.any():
      # each submission or weights String has lets say some impact on the global model represented by avg_weights[i]
      new_weights += np.array(submission) * (avg_weights[i] / total_weights)
  return new_weights




def accuracy_based(submissions, model , test_dataloader, criterion):
   
    scores = []
    for i, submission in enumerate(submissions):

        if len(submission)>0:
            model.set_weights(model,submission)
            local_model_accuracy = calculate_accuracy(model , test_dataloader, criterion)

            scores.append(local_model_accuracy) 
        else:
            scores.append(0)

    interaction_type = calculate_differences(scores)
    converted_adjusted_normalized_scores = [float_to_int(value,1e18) for value in scores]
    return converted_adjusted_normalized_scores , interaction_type



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
       
        ##similarities.append(limitcomma(similarity,5))
        similarities.append(similarity)

    ## here remove it later
    ##similarities = [10.49442, 10.62045, 7.10532, 12.89865, 7.32139, 7.21562, 7.58054]
    ##similarities = [ limitcomma(similarity,8) for similarity in similarities ]
    weights_loader = IpfsWeightsLoader()
    with open('yep.txt', 'a') as f:
        f.write(f"{similarities}   {trainers}\n") 

    model_loader = IpfsModelLoader(weights_loader)
    model = model_loader.load(global_model_hash) 
    fed_avg_aggregator = aggregation_algorithms.FedAvgAggregator(ModelLoaders.Model(model).count, weights_loader)

    normalized_scores = fed_avg_aggregator.calculate_normalized_weights(similarities)
    adjusted_normalized_scores = fed_avg_aggregator.calculate_adjusted_min_max_normalized_scores(similarities)

    

    converted_similarities = [float_to_int(value) for value in similarities]
    converted_adjusted_normalized_scores = [float_to_int(value) for value in adjusted_normalized_scores]
    with open('mimi.txt', 'a') as f:
        f.write(f"the original scores  : {similarities}\n") 
        f.write(f"the normalized similarity scores  : {normalized_scores}\n") 
        f.write(f"the adjusted normalized similarity scores  : {adjusted_normalized_scores}\n") 
        f.write(f"the converted adjusted normalized similarity scores  : {converted_adjusted_normalized_scores}\n") 



    return converted_adjusted_normalized_scores


def limitcomma(value, limit=2):
  v = str(value).split(".")
  return float(v[0]+"."+v[1][:limit])


# gets smth stored on ipfs using its hash
def get_model_weights(hash):

    #client = ipfshttpclient.connect(host='localhost', port=5001)
    client = ipfshttpclient.connect('/ip4/0.0.0.0/tcp/5001')
    stream = client.cat(hash)
    return stream

# gets smth stored on ipfs using its hash
def get_all_weights(hash):
    #client = ipfshttpclient.connect(host='localhost', port=5001)
    client = ipfshttpclient.connect('/ip4/0.0.0.0/tcp/5001')
    stream = client.cat(hash)
    return stream

def replace_nan_with_random(array, low, high):


    mask = np.isnan(array)
    array[mask] = np.random.uniform(low, high, size=np.count_nonzero(mask))
    return array
   



def perturb_array(original_array, perturbation_factor):
    perturbed_array = []
    for weight in original_array:
        perturbation = random.uniform(-perturbation_factor, perturbation_factor)
        new_weight = weight + perturbation
        perturbed_array.append(new_weight)
    return perturbed_array


def random_model(original_array):
    # Generate random weights with the same length as original_array
    random_weights = [random.uniform(0, 1) for _ in range(len(original_array))]
    return random_weights


def calculate_differences(accuracies):


  # Sort accuracies in descending order
  sorted_accuracies = np.sort(accuracies)[::-1]

  # Determine the index of the top 2/3 elements
  cutoff = int(len(sorted_accuracies) * 2 / 3)

  # Calculate the mean of the top 2/3 accuracies
  mean_top_acc = np.mean(sorted_accuracies[:cutoff])

  # Calculate differences
  differences = [acc - mean_top_acc for acc in accuracies]
  differences = [float(diff) for diff in differences]

  differences = [1 if x > 0 or x >= -0.2 else 0 for x in differences]

  return differences


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8089', threaded=True)
