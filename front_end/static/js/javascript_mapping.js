const localhost = "localhost";
const apiPort = 5000;

// Create the map object and set the initial view
const myMap = L.map("map", {
    center: [0, 0],
    zoom: 3
});

// Add a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18
}).addTo(myMap);

// Create a marker cluster group
let markers = L.markerClusterGroup({
    disableClusteringAtZoom: 3
});

const getBaseUrl = () => `http://${localhost}:${apiPort}/api`;
const getEndpointUrl = (endpoint) => `${getBaseUrl()}/${endpoint}`;
const getYearsUrl = () => getEndpointUrl("years");
const getCountriesUrl = () => getEndpointUrl("country");
const getCountryLocationsUrl = () => getEndpointUrl("country/location");
const getTableYearUrl = (year) => getEndpointUrl(`table/year/${year}`);

// Function to dynamically populate the year dropdown and load data
const initializeDropdownAndData = () => {
    const yearsUrl = getYearsUrl();
    fetch(yearsUrl)
    .then(response => response.json())
    .then(years => {
        const yearSelect = document.getElementById("yearSelect");
        years.forEach(year => {
            const option = document.createElement("option");
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        });

        loadMarkersForYearAndType(years[0], 'happiness');

        // Add event listener for year changes
        yearSelect.addEventListener('change', (event) => {
            const selectedYear = parseInt(event.target.value);
            const selectedDataType = document.getElementById('dataTypeSelect').value;
            loadMarkersForYearAndType(selectedYear, selectedDataType);
        });

        // Add event listener for data type changes
        const dataTypeSelect = document.getElementById('dataTypeSelect');
        dataTypeSelect.addEventListener('change', (event) => {
            const selectedYear = parseInt(yearSelect.value);
            const selectedDataType = event.target.value;
            loadMarkersForYearAndType(selectedYear, selectedDataType);
        });
    })
    .catch(error => console.error("Error initializing map.", error));
}

function hexToRgb(hex) {
    // Remove the '#' if present
    hex = hex.replace(/^#/, '');

    // Parse the hex string and return an RGB object
    const bigint = parseInt(hex, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;

    return { r, g, b };
}

function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase();
}

function interpolateColor(color1, color2, t) {
    // Convert hex to RGB
    const colorA = hexToRgb(color1);
    const colorB = hexToRgb(color2);

    // Interpolate RGB values
    const r = Math.round((1 - t) * colorA.r + t * colorB.r);
    const g = Math.round((1 - t) * colorA.g + t * colorB.g);
    const b = Math.round((1 - t) * colorA.b + t * colorB.b);

    // Convert back to hex
    return rgbToHex(r, g, b);
}

function interpolateGradient(colors, t) {
    const n = colors.length - 1;

    // Get whole part (index) and fractional part for interpolation
    const index = Math.floor(t);  // Whole part
    const frac = t - index;       // Fractional part

    // Clamp index within bounds of the colors array
    const colorA = colors[Math.max(0, Math.min(index, n))];
    const colorB = colors[Math.max(0, Math.min(index + 1, n))];

    // Interpolate between colorA and colorB
    return interpolateColor(colorA, colorB, frac);
}

function getColorForValueHelper(points, value) {
    // Sort points by the value in descending order
    points.sort((a, b) => b.value - a.value);

    // Handle edge cases
    if (value <= points[points.length - 1].value) {
        return points[points.length - 1].color;
    }
    if (value >= points[0].value) {
        return points[0].color;
    }

    // Find the two surrounding points
    let lowerPoint, upperPoint;
    for (let i = 0; i < points.length - 1; i++) {
        if (value <= points[i].value && value >= points[i + 1].value) {
            lowerPoint = points[i + 1];
            upperPoint = points[i];
            break;
        }
    }

    // Interpolate the color between the two points
    const t = (value - lowerPoint.value) / (upperPoint.value - lowerPoint.value);
    return interpolateColor(lowerPoint.color, upperPoint.color, t);
}

// Function to get a color based on the value
function getColorForValue(value, type) {
    const green = '#2ECC71';
    const yellow = '#F1C40F';
    const orange = '#E67E22';
    const red = '#E74C3C';

    let gradient = [
        {value: 7, color: green},
        {value: 5, color: yellow},
        {value: 3, color: orange},
        {value: 0, color: red}
    ];

    if (type === 'happiness') {
        gradient = [
            {value: 7, color: green},
            {value: 5, color: yellow},
            {value: 3, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'gdp') {
        gradient = [
            {value: 11, color: green},
            {value: 9, color: yellow},
            {value: 3, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'social_support') {
        gradient = [
            {value: 0.8, color: green},
            {value: 0.6, color: yellow},
            {value: 0.4, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'life_expectancy') {
        gradient = [
            {value: 70, color: green},
            {value: 60, color: yellow},
            {value: 50, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'freedom') {
        gradient = [
            {value: 0.7, color: green},
            {value: 0.5, color: yellow},
            {value: 0.3, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'generosity') {
        gradient = [
            {value: 0.3, color: green},
            {value: 0.2, color: yellow},
            {value: 0.1, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'corruption') {
        gradient = [
            {value: 0.7, color: red},
            {value: 0.5, color: orange},
            {value: 0.3, color: yellow},
            {value: 0, color: green}
        ];
    } else if (type === 'positive_affect') {
        gradient = [
            {value: 0.6, color: green},
            {value: 0.5, color: yellow},
            {value: 0.4, color: orange},
            {value: 0, color: red}
        ];
    } else if (type === 'negative_affect') {
        gradient = [
            {value: 0.4, color: red},
            {value: 0.3, color: orange},
            {value: 0.2, color: yellow},
            {value: 0, color: green}
        ];
    }
    return getColorForValueHelper(gradient, value);
}

// Function to load and display markers for a specific year and data type
function loadMarkersForYearAndType(year, type) {
    markers.clearLayers();

    const locationsUrl = getCountryLocationsUrl();
    const tableUrl = getTableYearUrl(year);

    fetch(locationsUrl)
    .then(response => response.json())
    .then(locations => {
        fetch(tableUrl)
        .then(response => response.json())
        .then(data => {
            const filteredData = data.filter(item => item.year === year);

            filteredData.forEach(item => {
                const country = item["Country name"];
                const location = locations[country];
                const latitude = location?.[0];
                const longitude = location?.[1];

                if (latitude && longitude) {
                    let value;
                    let popupContent;
                    
                    if (type === 'happiness') {
                        value = item["Life Ladder"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Happiness Score: ${value}`;
                    } 
                    else if (type === 'gdp') {
                        value = item["Log GDP per capita"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Log GDP per Capita: ${value}`;
                    } 
                    else if (type === 'social_support') {
                        value = item["Social support"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Social Support: ${value}`;
                    } 
                    else if (type === 'life_expectancy') {
                        value = item["Healthy life expectancy at birth"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Life Expectancy: ${value}`;
                    } 
                    else if (type === 'freedom') {
                        value = item["Freedom to make life choices"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Freedom: ${value}`;
                    } 
                    else if (type === 'generosity') {
                        value = item["Generosity"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Generosity: ${value}`;
                    } 
                    else if (type === 'corruption') {
                        value = item["Perceptions of corruption"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Perceptions of Corruption: ${value}`;
                    } 
                    else if (type === 'positive_affect') {
                        value = item["Positive affect"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Positive Affect: ${value}`;
                    } 
                    else if (type === 'negative_affect') {
                        value = item["Negative affect"];
                        popupContent = `<b>${country}</b><br>Year: ${year}<br>Negative Affect: ${value}`;
                    }

                    const color = getColorForValue(value, type);

                    const marker = L.circleMarker([latitude, longitude], {
                        radius: 15,
                        fillColor: color,
                        color: '#000',
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    }).bindTooltip(popupContent, { permanent: false, direction: 'top' });

                    markers.addLayer(marker);
                } else {
                    console.warn(`No coordinates for country: ${country}`);
                }
            });

            myMap.addLayer(markers);
        });
    })
    .catch(error => console.error("Error", error));
}

// Initialize the dropdown and load the initial data
initializeDropdownAndData();
