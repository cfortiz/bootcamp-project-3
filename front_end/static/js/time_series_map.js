// Initialize a Leaflet map
const map = L.map('map').setView([20, 0], 2);

// Add a tile layer to the map using OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Load GeoJSON data
async function loadGeoJSON() {
    const response = await fetch('https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson');
    if (!response.ok) {
        throw new Error('Failed to load GeoJSON data');
    }
    return await response.json();
}

// Fetch happiness data from JSON
async function fetchData() {
    const response = await fetch('worldHappiness.table.json');
    if (!response.ok) {
        console.error('Failed to load samples.json:', response.status);
        return;
    }
    const data = await response.json();

    const countryData = {};
    data.forEach(item => {
        const countryName = item['Country name'];
        const year = item.year;
        const lifeLadder = item['Life Ladder'];

        if (!countryData[year]) {
            countryData[year] = {};
        }
        if (!countryData[year][countryName]) {
            countryData[year][countryName] = [];
        }
        countryData[year][countryName].push(lifeLadder);
    });

    const geoJsonData = await loadGeoJSON();
    let years = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023];
    let currentYearIndex = 0;

    // Reference to the legend element
    const legend = document.getElementById('legend');

    // Store the interval ID
    let updateInterval;

    // Function to start the map updates
    function startUpdates() {
        updateInterval = setInterval(() => {
            const year = years[currentYearIndex];
            loadMapForYear(countryData, geoJsonData, year);
            legend.textContent = `Year: ${year}`;
            currentYearIndex = (currentYearIndex + 1) % years.length;
        }, 200);

        // Show stop icon, hide play icon
        document.getElementById('stopButton').style.display = 'inline';
        document.getElementById('playButton').style.display = 'none';
    }

    // Function to stop the map updates
    function stopUpdates() {
        clearInterval(updateInterval);

        // Show play icon, hide stop icon
        document.getElementById('playButton').style.display = 'inline';
        document.getElementById('stopButton').style.display = 'none';
    }

    // Add event listeners to the icons
    document.getElementById('playButton').addEventListener('click', () => {
        startUpdates();
    });

    document.getElementById('stopButton').addEventListener('click', () => {
        stopUpdates();
    });

    // Start fetching data and set up initial updates
    startUpdates();
}

// Function to load the map for a specific year
function loadMapForYear(countryData, geoJsonData, year) {
    map.eachLayer((layer) => {
        if (layer instanceof L.GeoJSON) {
            map.removeLayer(layer);
        }
    });

    const yearData = countryData[year];
    const color = d3.scaleLinear()
        .domain([1, 10])
        .range(["red", "green"]);

    geoJsonData.features.forEach(feature => {
        const countryName = feature.properties.name;
        const scores = yearData[countryName];

        if (scores) {
            const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;

            // Create a GeoJSON layer with tooltip
            const geoJsonLayer = L.geoJSON(feature, {
                style: {
                    fillColor: color(avgScore),
                    weight: 1,
                    opacity: 1,
                    color: 'white',
                    fillOpacity: 0.7
                }
            });

            // Bind tooltip with country name and average happiness score
            geoJsonLayer.bindTooltip(`${countryName}: ${avgScore.toFixed(2)}`, {
                permanent: false,
                direction: 'auto'
            });

            // Add the layer to the map
            geoJsonLayer.addTo(map);
        }
    });
}

// Start the process
fetchData();