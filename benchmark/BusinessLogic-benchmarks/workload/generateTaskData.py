# import json
# import random
# import string

# def generate_random_string(length):
#     # Define the characters to choose from (letters and digits)
#     characters = string.ascii_letters + string.digits
#     # Generate a random string using random.choices
#     random_string = ''.join(random.choices(characters, k=length))
#     return random_string

# def generate_data(n):
#     data = []
#     for _ in range(n):
#         _modelCID = generate_random_string(20) 
#         _infoCID = generate_random_string(20)  
     
#         maxRounds = random.randint(20, 50)
#         requiredTrainers = random.randint(10, 20)

#         item = {
#             "_modelCID": _modelCID,
#             "_infoCID": _infoCID,
#             "maxRounds": maxRounds,
#             "requiredTrainers": requiredTrainers
#         }
#         data.append(item)
    
#     return data

# def main():
#     n = 25  # Number of items to generate
#     generated_data = generate_data(n)

#     # Write to JSON file
#     with open('publishTaskWorkload.json', 'w') as json_file:
#         json.dump(generated_data, json_file, indent=4)


#     # Load the JSON data from a file
#     with open('publishTaskWorkload.json', 'r') as file:
#         data = json.load(file)

#     # Now 'data' is a Python list containing dictionaries
#     print(data)
# if __name__ == "__main__":
#     main()


data = [
    {
        "_modelCID": "3XfxoqYkfGXDQ3bqSyCh",
        "_infoCID": "5r4SgvOUlMTrdP64GHZ3",
        "maxRounds": 23,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "B3O04kPxBMFeJhXPhIYm",
        "_infoCID": "dAQQ9DarvmhmsmM11yQc",
        "maxRounds": 40,
        "requiredTrainers": 18
    },
    {
        "_modelCID": "Fz3jS9Gr9R3txPcHpWi2",
        "_infoCID": "Y6aoMJ867ZxNWiw6LNAJ",
        "maxRounds": 43,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "hunz8RDc8ZbxcM8XUy3x",
        "_infoCID": "vWTQpG2njWJn4kt69WDe",
        "maxRounds": 34,
        "requiredTrainers": 18
    },
    {
        "_modelCID": "GWHdcTtH4QInx9EwYG32",
        "_infoCID": "fILSpbCyrzuW11Axwqc7",
        "maxRounds": 27,
        "requiredTrainers": 19
    },
    {
        "_modelCID": "iSg8eIZdDj4Kc1WdtRe8",
        "_infoCID": "xzz3eIltkv0PkxMm1V5q",
        "maxRounds": 36,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "kwBp3vwtk6SD8bbFQv3u",
        "_infoCID": "pUMSau0XKLfMihvf1uaa",
        "maxRounds": 32,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "wj88Sf2XXpbnL11YkQvB",
        "_infoCID": "QxDhSiFWFAuS2qumez0p",
        "maxRounds": 40,
        "requiredTrainers": 15
    },
    {
        "_modelCID": "PHpmtffqQtl75dhx7epC",
        "_infoCID": "zDSeUNvnMsh9gtxHwP9n",
        "maxRounds": 45,
        "requiredTrainers": 14
    },
    {
        "_modelCID": "D88wzT4IPPxMz5eiKVQQ",
        "_infoCID": "XkCWLJdoGCn8fnyXklSq",
        "maxRounds": 44,
        "requiredTrainers": 17
    },
    {
        "_modelCID": "h1eWVMR4k7eTjD7r5lVq",
        "_infoCID": "KKndk6ltvr58UzP3Kpt0",
        "maxRounds": 36,
        "requiredTrainers": 16
    },
    {
        "_modelCID": "vrkIZr3BAGQoVGNAbZzq",
        "_infoCID": "wTWXSoU6MuCOZarUg9PD",
        "maxRounds": 29,
        "requiredTrainers": 13
    },
    {
        "_modelCID": "KqXEhoPW7zx7LRvTlD73",
        "_infoCID": "g5emvKD05q2fAtU1GBWY",
        "maxRounds": 27,
        "requiredTrainers": 16
    },
    {
        "_modelCID": "h1AdbBijerta74zI6Gz6",
        "_infoCID": "8xuHDpaX188jOb9zbb8T",
        "maxRounds": 25,
        "requiredTrainers": 17
    },
    {
        "_modelCID": "SFHgrGOrKrRD2Zy08dBI",
        "_infoCID": "sobqKFacwt2PoaZGV5j5",
        "maxRounds": 44,
        "requiredTrainers": 12
    },
    {
        "_modelCID": "uOs8JfViK0m7ulh8Effq",
        "_infoCID": "2JYeHDhNNKAOOO5D6ty0",
        "maxRounds": 45,
        "requiredTrainers": 15
    },
    {
        "_modelCID": "rM8WguJZa5waKW8awGgQ",
        "_infoCID": "mpAK4To6XDrMOw1IQiJo",
        "maxRounds": 21,
        "requiredTrainers": 11
    },
    {
        "_modelCID": "iMqAZh3u0R5FAPd0H0MU",
        "_infoCID": "Ku8SX0czvxQoyPZxty4F",
        "maxRounds": 31,
        "requiredTrainers": 12
    },
    {
        "_modelCID": "9j3BBTJlQ1m0VtkEn6Wl",
        "_infoCID": "paa2K1oFolkpJrTPGx7B",
        "maxRounds": 49,
        "requiredTrainers": 11
    },
    {
        "_modelCID": "EfaR7KRL1PW04hXcs07W",
        "_infoCID": "er7NHlRDL0L23RweBMa1",
        "maxRounds": 28,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "xngR0SJrpjxnAysi9kE3",
        "_infoCID": "19cn6xlHtAvkOQeXG9C8",
        "maxRounds": 21,
        "requiredTrainers": 15
    },
    {
        "_modelCID": "oCACzczGdzldUVlVGxyo",
        "_infoCID": "PnGnDWQaCiIMapTXhG18",
        "maxRounds": 28,
        "requiredTrainers": 13
    },
    {
        "_modelCID": "bWTCqHk2HSLJClz25wXO",
        "_infoCID": "ErhnVWAZ4iRcM4P8Zkv9",
        "maxRounds": 50,
        "requiredTrainers": 10
    },
    {
        "_modelCID": "hlnTfeoJe4yRpfPp97Bt",
        "_infoCID": "pha7crYHY47l6BCgE1ad",
        "maxRounds": 41,
        "requiredTrainers": 20
    },
    {
        "_modelCID": "Gle4YABwZklzuR92HfaD",
        "_infoCID": "1q9IFLzygqLirki4Vdhx",
        "maxRounds": 43,
        "requiredTrainers": 19
    }
]

# Extracting the values into separate lists
model_cids = [item["_modelCID"] for item in data]
info_cids = [item["_infoCID"] for item in data]
max_rounds = [item["maxRounds"] for item in data]
required_trainers = [item["requiredTrainers"] for item in data]

# Write the arrays to a file in array format
with open('tasks.txt', 'w') as file:
    file.write("Model CIDs: [\n")
    file.write(',\n'.join(f'    "{cid}"' for cid in model_cids) + '\n]\n\n')
    file.write("Info CIDs: [\n")
    file.write(',\n'.join(f'    "{cid}"' for cid in info_cids) + '\n]\n\n')
    file.write("Max Rounds: [\n")
    file.write(',\n'.join(map(str, max_rounds)) + '\n]\n\n')
    file.write("Required Trainers: [\n")
    file.write(',\n'.join(map(str, required_trainers)) + '\n]\n')

print("Data written to tasks.txt")
