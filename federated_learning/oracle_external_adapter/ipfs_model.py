import os
import tempfile
import torch
from model import Model
import pickle

class IpfsModelLoader():
  def __init__(self, weights_loader, ipfs_api = '/ip4/127.0.0.1/tcp/5001') -> None:
    self.weights_loader = weights_loader
    self.ipfs_api = ipfs_api
    pass

  def load(self, model_cid, weights_cid = ""):
    with tempfile.TemporaryDirectory() as tempdir:
      model_path = os.path.join(tempdir, 'model.h5')
      print(model_path)
      os.system(f"ipfs get --api {self.ipfs_api} -o {model_path} {model_cid}")
      loaded_data = torch.load(model_path)
      model = loaded_data
      if weights_cid != "":
        weights = self.weights_loader.load(weights_cid)


        model.set_weights(model,weights)
    return loaded_data
  




