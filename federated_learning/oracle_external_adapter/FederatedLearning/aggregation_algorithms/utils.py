import numpy as np
import ast




# FedAvg
def weighted_fed_avg(submissions, model_size, avg_weights):
  total_weights = np.sum(avg_weights)
  new_weights = np.zeros(model_size)

  for i, flattened_weights in enumerate(submissions):
    # each submission or weights String has lets say some impact on the global model represented by avg_weights[i]
    print("it happens before ", avg_weights)
    print("it happens here ", avg_weights[i] / total_weights)
    flattened_weights = np.array(flattened_weights)
    if flattened_weights.size > 0:
      new_weights += flattened_weights * (avg_weights[i] / total_weights)

  return new_weights


#FedProx
def prox_agg(submissions, model_size, weights_loader, avg_weights , proximal_coefficient, global_model_weights):
    total_weights = np.sum(avg_weights)
    new_weights = np.zeros(model_size)

    for i, submission in enumerate(submissions):
        (_, _, _, weights_cid) = submission
        # Calculate the proximal term for the individual client's weights
        prox_term = calculate_prox_term(global_model_weights, weights, proximal_coefficient)
        # load weights from ipfs
        weights = weights_loader.load(weights_cid)
        # Add the proximal term to address the problem occuring when a local update diverges from the previous global model
        new_weights += weights * (avg_weights[i] / total_weights) + prox_term

    return new_weights

## In a federated learning scenario, each client calculates its own proximal term based on its local model weights and the central model weights
def calculate_prox_term(global_model_weights, local_model_weights, proximal_coefficient):
    # Calculate the proximal term as the L2 norm of the difference between
    # the local model weights and the central model weights, multiplied by
    # the proximal coefficient.
    prox_term = proximal_coefficient * np.linalg.norm(local_model_weights - global_model_weights)
    return prox_term

