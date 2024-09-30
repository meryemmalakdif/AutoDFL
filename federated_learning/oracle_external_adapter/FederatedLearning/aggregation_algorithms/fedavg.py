from .utils import *

class FedAvgAggregator():
  def __init__(self, model_size, weights_loader):
    self.model_size = model_size
    self.weights_loader = weights_loader

  def aggregate(self, submissions  , scores):
    #samples = [samples for (_, _, samples, _,_) in submissions]
    # the impact a specific model update has when aggregating is measured based on its data size
    for element in scores:
      print(type(element))
    print("scores ", scores)
    normalized_scores = self.calculate_normalized_weights(scores)
    # for index, fruit in enumerate(normalized_scores):
    #   with open('dad.txt', 'a') as f:
    #     f.write(f"{normalized_scores[index]}     \n") 
    # refactor ya bent
    return weighted_fed_avg(submissions, self.model_size, normalized_scores)
  
  def calculate_normalized_weights(self,scores):
    min_score = min(scores)
    max_score = max(scores)
    normalized_weights = [(score - min_score) / (max_score - min_score) for score in scores]
    return normalized_weights
  
  def calculate_adjusted_min_max_normalized_scores(self,scores):
    min_score = min(scores)
    max_score = max(scores)
    new_max = 0.6
    new_min = 0.3
    normalized_scores = [((1 - (score - min_score) / (max_score - min_score)) * (new_max - new_min) + new_min) for score in scores]
    return normalized_scores
  

  def calculate_adjusted_min_max_normalized_scores_marginal_gain(self, scores):
    # Find the absolute maximum value for normalization
    max_abs_score = max(abs(score) for score in scores)

    # Normalize scores to a range of -1 to 1
    normalized_scores = [(score / max_abs_score) for score in scores]

    # Shift and scale to the desired range of 0.01 to 0.99
    new_max = 0.99
    new_min = 0.01
    normalized_scores = [((1 + normalized_score) / 2) * (new_max - new_min) + new_min for normalized_score in normalized_scores]

    return normalized_scores

  def normalize_to_01_99(data):
    min_val = np.min(data)
    max_val = np.max(data)
    range_val = max_val - min_val

    normalized_data = (data - min_val) / range_val * 0.98 + 0.01

    return normalized_data