document.getElementById('led-on').addEventListener('click', function() {
    fetch('/led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: 'on' }),
    }).then(response => response.json()).then(data => {
        displayMessage('LED turned on');
    });
});

document.getElementById('led-off').addEventListener('click', function() {
    fetch('/led', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: 'off' }),
    }).then(response => response.json()).then(data => {
        displayMessage('LED turned off');
    });
});

async function fetchPredictions() {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ temp: 25 }),  // Example temperature value
    });
    const data = await response.json();
    document.getElementById('predicted-humidity').innerText = data.predicted_humidity;
    document.getElementById('predicted-temperature').innerText = data.predicted_temperature;
    displayMessage('Predictions updated');
}

// Fetch initial predictions
fetchPredictions();

const ctx = document.getElementById('dataChart').getContext('2d');
const dataChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],  // Populate with your data
        datasets: [
            {
                label: 'Temperature',
                data: [],  // Populate with your data
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            },
            {
                label: 'Humidity',
                data: [],  // Populate with your data
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            },
            {
                label: 'Predicted Temperature',
                data: [],  // Populate with your prediction data
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1,
                borderDash: [5, 5]
            },
            {
                label: 'Predicted Humidity',
                data: [],  // Populate with your prediction data
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                borderDash: [5, 5]
            }
        ]
    },
    options: {
        scales: {
            x: {
                beginAtZero: true
            },
            y: {
                beginAtZero: true
            }
        }
    }
});

function updateChart() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            dataChart.data.labels = data.timestamps;
            dataChart.data.datasets[0].data = data.temperatures;
            dataChart.data.datasets[1].data = data.humidities;
            dataChart.update();
        });
}

function displayMessage(message) {
    const messageContainer = document.getElementById('messages-container');
    const messageElement = document.createElement('p');
    messageElement.innerText = message;
    messageContainer.appendChild(messageElement);
}

// Fetch initial data and set interval for updating
updateChart();
setInterval(updateChart, 5000);  // Update chart every 5 seconds
