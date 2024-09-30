import os
import tempfile
import torch
from .model import Model
import pickle

class IpfsModelLoader():
  def __init__(self, weights_loader, ipfs_api = '/ip4/127.0.0.1/tcp/5001') -> None:
    self.weights_loader = weights_loader
    self.ipfs_api = ipfs_api
    pass

  def load(self, model_cid, weights_cid = ""):
    with tempfile.TemporaryDirectory() as tempdir:
      print("here am I ",tempdir)
      model_path = os.path.join(tempdir, 'model.h5')
      os.system(f"ipfs get --api {self.ipfs_api} -o {model_path} {model_cid}")
      loaded_data = torch.load(model_path)
      model = loaded_data
      print("loaded model from client ", model)
      # with open('milo.txt', 'a') as f:
      # # Write the submissions_evaluation to the file
      #   f.write(f"hello  : {loaded_data}\n") 
      # serialized_model = loaded_data['architecture']
      # serialized_state_dict = loaded_data['state_dict']
      # Deserialize the model architecture
      # model = pickle.loads(serialized_model)
   
      #print(model)
      # Deserialize the state dictionary
      # state_dict = pickle.loads(serialized_state_dict)
      #print(state_dict)


    if weights_cid != "":
      weights = self.weights_loader.load(weights_cid)
      model.set_weights(model,weights)

    return model



