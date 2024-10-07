import json
import random


def register_trainer():
    data = []
    # Load JSON data from the input file
    with open('./necessaryDataFiles/setTaskTrainersData.json', 'r') as input_file:
        data_trainers = json.load(input_file)

    i = 0
    for index in range(len(data_trainers)):
        item = {
            "task": index,
            "taskTrainers": data_trainers[index]['taskTrainers']
        }
        data.append(item)
        i+=1
    
    return data

def main():
    data = register_trainer()
    print(data)
    # Write to JSON file
    with open('./necessaryDataFiles/setTaskTrainersData.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()



