import json
import random

def generate_random_address():
    # Generate a random Ethereum address
    return '0x' + ''.join(random.choices('0123456789abcdef', k=40))

def generate_data():
    data = []
    # Load JSON data from the input file
    with open('./necessaryDataFiles/setTaskTrainersData.json', 'r') as input_file:
        data_trainers = json.load(input_file)

    
    for index in range(len(data_trainers)):
        for j in range(3):
            adr = data_trainers[index]['taskTrainers'][j]
            item = {
                "task": index,
                "adr": adr
            }
            data.append(item)

    
   

    return data

def main():
    generated_data = generate_data()

    # Write to JSON file
    with open('./necessaryDataFiles/SubjData.json', 'w') as json_file:
        json.dump(generated_data, json_file, indent=4)

if __name__ == "__main__":
    main()


