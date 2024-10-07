import json
import random

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_data(n):
    data = []
    for index in range(n):
        task = index  # Generate a random task ID
        taskTrainers = [] 
        for index in range(3):
            a = generate_random_address()  # Generate a random address for a trainer
            taskTrainers.append(a)
    
        item = {
            "task": task,
            "taskTrainers": taskTrainers
        }
        data.append(item)
    
    return data

def main():
    n = 10000  # Number of items to generate
    generated_data = generate_data(n)

    # Write to JSON file
    with open('setTaskTrainersData.json', 'w') as json_file:
        json.dump(generated_data, json_file, indent=4)

if __name__ == "__main__":
    main()
