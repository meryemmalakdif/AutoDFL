import os
import tempfile

class IpfsPictureLoader():
    def __init__(self, ipfs_api='/ip4/127.0.0.1/tcp/5001'):
        self.ipfs_api = ipfs_api

    # store picture on ipfs
    def store_picture(self, picture_path):
        # create a temporary directory that will be automatically cleaned up when the function finishes
        with tempfile.TemporaryDirectory() as tempdir:
            # copy the picture to the temporary directory
            temp_picture_path = os.path.join(tempdir, 'pic.png')
            os.system(f"cp {picture_path} {temp_picture_path}")

            # store the picture on ipfs
            response = os.popen(f'ipfs add --api {self.ipfs_api} -q {temp_picture_path}').read().strip()
            ipfs_hash = response.split('\n').pop()
            return ipfs_hash

# Example usage
        
# picture_path = 'pic.png'  # Path to your picture file
# ipfs_loader = IpfsPictureLoader()
# ipfs_hash = ipfs_loader.store_picture(picture_path)
# print("Picture stored on IPFS with hash:", ipfs_hash)
