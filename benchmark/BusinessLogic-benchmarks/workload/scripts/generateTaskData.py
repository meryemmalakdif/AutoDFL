import json
import random
import string

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_random_string(length):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits
    # Generate a random string using random.choices
    random_string = ''.join(random.choices(characters, k=length))
    return random_string



def generate_data(n):
    data = []
    for _ in range(n):
        _modelCID = generate_random_string(20)
        _infoCID = generate_random_string(20)
        maxRounds = 3
        requiredTrainers = 3

        item = {
            "_modelCID": _modelCID,
            "_infoCID": _infoCID,
            "maxRounds": maxRounds,
            "requiredTrainers": requiredTrainers
        }
        data.append(item)
    
    return data

def main():
    n = 1000000  # Number of items to generate
    generated_data = generate_data(n)

    # Write to JSON file
    with open('taskData.json', 'w') as json_file:
        json.dump(generated_data, json_file, indent=4)

if __name__ == "__main__":
    main()
