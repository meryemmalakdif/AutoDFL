import json
import random

# Function to update task data
def update_task_data(task):
    # Generate a random integer for '_interactionsTp' and assign it
    _interactionsTp = random.randint(1, 100)
    task['_interactionsTp'] = _interactionsTp
    
    # Remove the 'scores' field
    if 'scores' in task:
        del task['scores']
    
    # Replace 'totalRounds' with '_interactionsTpTa', a list of random ints
    _interactionsTpTa = [random.randint(0, _interactionsTp - 1) for _ in range(len(task['totalRounds']))]
    task['_interactionsTpTa'] = _interactionsTpTa
    
    if 'totalRounds' in task:
        del task['totalRounds']    
    return task

# Load JSON data from the input file
with open('objectiveReputationData.json', 'r') as input_file:
    data = json.load(input_file)

# Process each task in the array
for task in data:
    update_task_data(task)

# Write the updated JSON to the output file
with open('subjectiveReputationData.json', 'w') as output_file:
    json.dump(data, output_file, indent=4)

print("Data has been processed and written to 'output_data.json'.")
