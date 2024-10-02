import json
import random

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_data(n):
    data = []
    for _ in range(n):
        _taskId = random.randint(1, 1000)  # Generate a random task ID
        _taskPublisher = generate_random_address()  # Generate a random task publisher address
        # Generate arrays of random trainers, scores, and total rounds
        length = random.randint(3, 4)  # Random length for the arrays
        _trainers = [generate_random_address() for _ in range(length)]
        _scores = [random.randint(0, 100) for _ in range(length)]
        totalRounds = [random.randint(1, 10) for _ in range(length)]

        item = {
            "taskId": _taskId,
            "taskPublisher": _taskPublisher,
            "trainers": _trainers,
            "scores": _scores,
            "totalRounds": totalRounds
        }
        data.append(item)
    
    return data

def main():
    n = 10000  # Number of items to generate
    generated_data = generate_data(n)

    # Write to JSON file
    with open('objectiveReputationData.json', 'w') as json_file:
        json.dump(generated_data, json_file, indent=4)

if __name__ == "__main__":
    main()
