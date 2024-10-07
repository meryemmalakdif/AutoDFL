import json
import random

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_data(n):
    data = []
    # Load JSON data from the input file
    with open('./subjectiveRep/trainersSubj.json', 'r') as input_file:
        data_trainers = json.load(input_file)

    i = 0
    for index in range(n):
        task = index  # Generate a random task ID
        taskTrainers = data_trainers[i]['taskTrainers']
        i+=1 
        item = {
            "task": task,
            "taskTrainers": taskTrainers
        }
        data.append(item)
        if i == len(data_trainers):
            i=0
    
    return data

def main():
    n = 300  # Number of items to generate
    generated_data = generate_data(n)

    # Write to JSON file
    with open('./subjectiveRep/setTaskTrainersData.json', 'w') as json_file:
        json.dump(generated_data, json_file, indent=4)

if __name__ == "__main__":
    main()



