import json
import random

# Function to update task data
def get_data(item):
    # Generate a random integer for '_interactionsTp' and assign it
    

    taskId = item['task']
    trainers = item['taskTrainers']
    scores = [random.randint(100000000000000000, 150000000000000000) for _ in range(3)]
    ## turn into array of string because ether needs to get big numbers as string and then convert them
    scores = [str(score) for score in scores ]
    totalRounds = [random.randint(1, 3) for _ in range(3)]

    item['taskId'] = taskId
    item['trainers'] = trainers
    item['scores'] = scores
    item['totalRounds'] = totalRounds    

    if 'task' in item:
        del item['task']
    if 'taskTrainers' in item:
        del item['taskTrainers']

    return item

# Load JSON data from the input file
with open('./necessaryDataFiles/setTaskTrainersData.json', 'r') as input_file:
    data = json.load(input_file)

# Process each task in the array
for item in data:
    get_data(item)

# Write the updated JSON to the output file
with open('./necessaryDataFiles/objectiveReputationData.json', 'w') as output_file:
    json.dump(data, output_file, indent=4)

print("Data has been processed and written to 'objectiveReputationData.json'.")
