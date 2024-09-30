const fs = require('fs'); // Import the file system module

// Existing array
let tasks = [
  {
    "task": 12,
    "trainers": [
      "0xffshjkhgdsfjkghnskdfgd", // Example Ethereum address
      "0xgesr" // Example Ethereum address
    ],
    "round": 5
  },
];

// Function to generate a random Ethereum address
function getRandomEthereumAddress() {
  const characters = '0123456789abcdef'; // Hexadecimal characters
  let address = '0x'; // Ethereum addresses start with '0x'
  for (let i = 0; i < 40; i++) { // 40 hex characters
    address += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return address;
}

// Function to add a random task
function addRandomTask() {
  const newTask = {
    task: Math.floor(Math.random() * 100), // Random task number between 0 and 99
    trainers: [
      getRandomEthereumAddress(), // Generate a random Ethereum address
      getRandomEthereumAddress()  // Generate another random Ethereum address
    ],
    round: Math.floor(Math.random() * 10) // Random round number between 0 and 9
  };

  tasks.push(newTask); // Add the new task to the array
}

// Add 10,000 random tasks
for (let i = 0; i < 30000; i++) {
  addRandomTask();
}

// Write the updated tasks array to a JSON file
fs.writeFile('meryem.json', JSON.stringify(tasks, null, 2), (err) => {
  if (err) {
    console.error('Error writing to file', err);
  } else {
    console.log('Tasks successfully written to meryem.json');
  }
});
