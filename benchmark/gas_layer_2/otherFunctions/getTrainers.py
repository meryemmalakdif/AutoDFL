import json
import random

# Function to update task data
def get_data(item):
    # Generate a random integer for '_interactionsTp' and assign it
    

    trainers = item['trainers']

    item['trainers'] = trainers
  

    if 'taskId' in item:
        del item['taskId']
    if 'scores' in item:
        del item['scores']
    if 'totalRounds' in item:
        del item['totalRounds']
    return item

# Load JSON data from the input file
with open('./objectiveReputationData.json', 'r') as input_file:
    data = json.load(input_file)

# Process each task in the array
for item in data:
    get_data(item)

# Write the updated JSON to the output file
with open('./trainers.json', 'w') as output_file:
    json.dump(data, output_file, indent=4)

