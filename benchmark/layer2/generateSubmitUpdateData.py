import json
import random
import hashlib

# Function to generate a random hash
def generate_random_hash():
    return hashlib.sha256(str(random.random()).encode()).hexdigest()

# Create an array of 25 elements with random data
data = []
for task_id in range(10000):  # Loop from 0 to 24 for 25 elements
    element = {
        "task": task_id,  # Use the loop index as the task ID
        "update": {
            "trainingAccuracy": random.randint(0, 100),  # Random accuracy between 0 and 100
            "trainingDataPoints": random.randint(100, 1000),  # Random data points between 100 and 1000
            "weights": generate_random_hash()  # Random hash
        },
        "round": random.randint(1, 10)  # Random round between 1 and 10
    }
    data.append(element)

# Write the array to a JSON file
with open('random_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data written to random_data.json")
