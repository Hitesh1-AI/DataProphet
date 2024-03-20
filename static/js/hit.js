async function startTraining() {
    const response = await fetch('/start-training', {
        method: 'GET'
    });
    // Handle response as needed
}

// Call startTraining function when a button is clicked or any other event occurs
document.getElementById('start-training-button').addEventListener('click', startTraining);
