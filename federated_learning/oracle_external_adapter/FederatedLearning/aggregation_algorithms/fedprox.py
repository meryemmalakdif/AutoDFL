from .utils import *

class FedProxAggregator():
  def __init__(self, model_size, weights_loader,proximal_coefficient, global_model_weights):
    self.model_size = model_size
    self.weights_loader = weights_loader
    self.proximal_coefficient = proximal_coefficient
    self.global_model_weights = global_model_weights

  def aggregate(self, trainers, submissions, scorers = None, scores = None):
    samples = [samples for (_, _, samples, _) in submissions]
    # the impact a specific model update has when aggregating is measured based on its data size
    return prox_agg(submissions, self.model_size, self.weights_loader, samples , self.proximal_coefficient , self.global_model_weights)
