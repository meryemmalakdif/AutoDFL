const fs = require('fs');

// Replace 'yourfile.json' with the name of your JSON file
const filePath = 'publishTaskWorkload.json';

// Read the JSON file
fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }

    try {
        // Parse the JSON data
        const jsonArray = JSON.parse(data);

        // Check if the parsed data is an array
        if (Array.isArray(jsonArray)) {
            // Loop through each element and delete the 'requiredAggregators' field
            jsonArray.forEach(element => {
                delete element.requiredAggregators;
            });

            // Convert the updated array back to JSON
            const updatedData = JSON.stringify(jsonArray, null, 2); // Pretty print with 2 spaces

            // Write the updated JSON back to the file
            fs.writeFile(filePath, updatedData, 'utf8', (err) => {
                if (err) {
                    console.error('Error writing the file:', err);
                } else {
                    console.log('File updated successfully!');
                }
            });
        } else {
            console.error('The JSON data is not an array.');
        }
    } catch (parseErr) {
        console.error('Error parsing the JSON data:', parseErr);
    }
});
