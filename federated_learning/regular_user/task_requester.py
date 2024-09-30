import torch
import os
import tempfile
import pickle
import subprocess


class TaskRequester:
    def __init__(self, ipfs_api='/ip4/127.0.0.1/tcp/5001'):
        self.ipfs_api = ipfs_api

    def selectTrainers(self,list,n):
        if n >= len(list):
            return list
        else:
            return list[:n]

    def serialize_and_save_model(self, model, model_info, model_path='model_data.pth', info_path='model_info.txt'):
        torch.save(model, model_path)
        with open(info_path, 'w') as file:
            file.write(model_info)
        return model_path, info_path

    
    def save_model(self, model, model_info, model_path='model_data.pkl', info_path='model_info.txt'):
        serialized_model = pickle.dumps(model)
        state_dict = model.state_dict()
        serialized_state_dict = pickle.dumps(state_dict)
        with open('model_data.pkl', 'wb') as f:
            torch.save({
                'architecture': serialized_model,
                'state_dict': serialized_state_dict
            }, f)
        #torch.save(model.state_dict(), model_path)
        with open(info_path, 'w') as file:
            file.write(model_info)
        return model_path, info_path
    
# json_string = model.to_json()
# with open('model.json', 'w') as f:
#     f.write(json_string)


    # def load_model_and_info(model, model_path, info_path):
    #     # Load the model's state dictionary
    #     model.load_state_dict(torch.load(model_path))

    #     # Load additional model information
    #     model_info = torch.load(info_path)

    #     # Set the model to evaluation mode
    #     model.eval()

    #     return model, model_info

    # store picture on ipfs
    def store_model(self, model_path='model_data.pth', info_path='model_info.txt'):
        with tempfile.TemporaryDirectory() as tempdir:
            # Copy the model and info files to the temporary directory
            temp_model_path = os.path.join(tempdir, os.path.basename(model_path))
            temp_info_path = os.path.join(tempdir, os.path.basename(info_path))
            os.system(f'cp {model_path} {temp_model_path}')
            os.system(f'cp {info_path} {temp_info_path}')
         
          
            try:
                result = subprocess.run(
                    ['ipfs', 'add', '--api', self.ipfs_api, '-q', temp_model_path],
                    capture_output=True,
                    text=True,
                    check=True
                )
                model_response = result.stdout.strip()
                model_ipfs_hash = model_response.split('\n').pop()
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
                print(f"Error message: {e.stderr}")

            # Add the model file to IPFS
            model_response = os.popen(f'ipfs add --api {self.ipfs_api} -q {temp_model_path}').read().strip()
            model_ipfs_hash = model_response.split('\n').pop()

            # Add the info file to IPFS
            info_response = os.popen(f'ipfs add --api {self.ipfs_api} -q {temp_info_path}').read().strip()
            info_ipfs_hash = info_response.split('\n').pop()
            return model_ipfs_hash, info_ipfs_hash
        
    
    def retrieve_model_from_ipfs(self, model_ipfs_hash, info_ipfs_hash):
        with tempfile.TemporaryDirectory() as tempdir:
            # Download the model file from IPFS
            print("am here ",model_ipfs_hash)
            os.system(f'ipfs get --api {self.ipfs_api} {model_ipfs_hash} -o {tempdir}')
            downloaded_model_path = os.path.join(tempdir, model_ipfs_hash)

            os.system(f'ipfs get --api {self.ipfs_api} {info_ipfs_hash} -o {tempdir}')
            content_bytes = os.popen(f'ipfs cat --api {self.ipfs_api} {info_ipfs_hash}').read().encode('utf-8')
            content_str = content_bytes.decode('utf-8')
            #downloaded_info_path = os.path.join(tempdir, info_ipfs_hash)



            # Load the downloaded model file (assuming it's a PyTorch model)
            print(downloaded_model_path)
            loaded_data = torch.load(downloaded_model_path)
            serialized_model = loaded_data['architecture']
            serialized_state_dict = loaded_data['state_dict']
            # Deserialize the model architecture
            model = pickle.loads(serialized_model)
            #print(model)
             # Deserialize the state dictionary
            state_dict = pickle.loads(serialized_state_dict)
            #print(state_dict)
           
            return model, state_dict, content_str



    



# Example usage
# task_requester = TaskRequester()
# model_hash, info_hash = task_requester.store_model('path_to_model.pth', 'path_to_model_info.pth')
# print("Model IPFS Hash:", model_hash)
# print("Model Info IPFS Hash:", info_hash)
        
# model_ipfs_hash = 'your_model_ipfs_hash_here'
# info_ipfs_hash = 'your_info_ipfs_hash_here'
# retrieved_model, retrieved_info_path = task_requester.retrieve_model_from_ipfs(model_ipfs_hash, info_ipfs_hash)