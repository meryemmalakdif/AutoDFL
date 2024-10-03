import json
import time
import torch

class Aggregator():
  def __init__(self, weights_loader, aggregator):
    self.weights_loader = weights_loader
    self.aggregator = aggregator



  def aggregate(self, submissions, scores):
    new_weights = self.aggregator.aggregate(submissions , scores)
    weights_cid = self.weights_loader.store(new_weights)
    return weights_cid
  

