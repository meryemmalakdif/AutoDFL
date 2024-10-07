import json
import random


def register_trainer():
    data = []
    # Load JSON data from the input file
    with open('./subjectiveRep/trainersSubj.json', 'r') as input_file:
        data_trainers = json.load(input_file)

    i = 0
    for index in range(len(data_trainers)):
        element = data_trainers[index]['taskTrainers']
        for j in range(len(element)):
            item = {
                "trainer": element[j]
            }
            data.append(item)
    
    print(len(data))
    return data

def main():
    data = register_trainer()

    # Write to JSON file
    with open('./subjectiveRep/setTrainersData.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    main()



