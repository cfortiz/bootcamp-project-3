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

// Function to dynamically populate the year dropdown and load data
function initializeDropdownAndData() {
    fetch('worldHappiness.table.json')
        .then(response => response.json())
        .then(data => {
            const years = [...new Set(data.map(item => item.year))].sort();
            const yearSelect = document.getElementById('yearSelect');
            years.forEach(year => {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year;
                yearSelect.appendChild(option);
            });

            // Load markers for the initially selected year and data type
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
        .catch(error => console.error('Error loading the JSON data:', error));
}

// Function to get a color based on the value
function getColorForValue(value, type) {
    if (type === 'happiness') {
        return value > 7 ? '#2ECC71' :
               value > 5 ? '#F1C40F' :
               value > 3 ? '#E67E22' :
                           '#E74C3C';
    } 
    else if (type === 'gdp') {
        return value > 11 ? '#2ECC71' :
               value > 9 ? '#F1C40F' :
               value > 3 ? '#E67E22' :
                              '#E74C3C';
    } 
    else if (type === 'social_support') {
        return value > 0.8 ? '#2ECC71' :
               value > 0.6 ? '#F1C40F' :
               value > 0.4 ? '#E67E22' :
                             '#E74C3C';
    } 
    else if (type === 'life_expectancy') {
        return value > 70 ? '#2ECC71' :
               value > 60 ? '#F1C40F' :
               value > 50 ? '#E67E22' :
                             '#E74C3C';
    } 
    else if (type === 'freedom') {
        return value > 0.7 ? '#2ECC71' :
               value > 0.5 ? '#F1C40F' :
               value > 0.3 ? '#E67E22' :
                             '#E74C3C';
    } 
    else if (type === 'generosity') {
        return value > 0.3 ? '#2ECC71' :
               value > 0.2 ? '#F1C40F' :
               value > 0.1 ? '#E67E22' :
                             '#E74C3C';
    } 
    else if (type === 'corruption') {
        return value < 0.3 ? '#2ECC71' : // Low corruption is green
               value < 0.5 ? '#F1C40F' :
               value < 0.7 ? '#E67E22' :
                             '#E74C3C';  // High corruption is red
    } 
    else if (type === 'positive_affect') {
        return value > 0.6 ? '#2ECC71' :
               value > 0.5 ? '#F1C40F' :
               value > 0.4 ? '#E67E22' :
                             '#E74C3C';
    } 
    else if (type === 'negative_affect') {
        return value < 0.2 ? '#2ECC71' : // Low negative affect is green
               value < 0.3 ? '#F1C40F' :
               value < 0.4 ? '#E67E22' :
                             '#E74C3C';  // High negative affect is red
    }
}
// Function to load and display markers for a specific year and data type
function loadMarkersForYearAndType(year, type) {
    markers.clearLayers();

    fetch('worldHappiness.table.json')
        .then(response => response.json())
        .then(data => {
            const filteredData = data.filter(item => item.year === year);

            const countryCoordinates = {
                "Afghanistan": [33.93911, 67.709953],
                "Albania": [41.153332, 20.168331],
                "Algeria": [28.033886, 1.659626],
                "Andorra": [42.546245, 1.601554],
                "Angola": [-11.202692, 17.873887],
                "Antigua and Barbuda": [17.060816, -61.796428],
                "Argentina": [-38.416097, -63.616672],
                "Armenia": [40.069099, 45.038189],
                "Australia": [-25.274398, 133.775136],
                "Austria": [47.516231, 14.550072],
                "Azerbaijan": [40.143105, 47.576927],
                "Bahamas": [25.03428, -77.39628],
                "Bahrain": [26.0667, 50.5577],
                "Bangladesh": [23.684994, 90.356331],
                "Barbados": [13.193887, -59.543198],
                "Belarus": [53.709807, 27.953389],
                "Belgium": [50.503887, 4.469936],
                "Belize": [17.189877, -88.49765],
                "Benin": [9.30769, 2.315834],
                "Bhutan": [27.514162, 90.433601],
                "Bolivia": [-16.290154, -63.588653],
                "Bosnia and Herzegovina": [43.915886, 17.679076],
                "Botswana": [-22.328474, 24.684866],
                "Brazil": [-14.235004, -51.92528],
                "Brunei": [4.535277, 114.727669],
                "Bulgaria": [42.733883, 25.48583],
                "Burkina Faso": [12.238333, -1.561593],
                "Burundi": [-3.373056, 29.918886],
                "Cabo Verde": [16.002082, -24.013197],
                "Cambodia": [12.565679, 104.990963],
                "Cameroon": [7.369722, 12.354722],
                "Canada": [56.130366, -106.346771],
                "Central African Republic": [6.611111, 20.939444],
                "Chad": [15.454166, 18.732207],
                "Chile": [-35.675147, -71.542969],
                "China": [35.86166, 104.195397],
                "Colombia": [4.570868, -74.297333],
                "Comoros": [-11.6455, 43.3333],
                "Congo (Congo-Brazzaville)": [-0.228021, 15.827659],
                "Costa Rica": [9.748917, -83.753428],
                "Croatia": [45.1, 15.2],
                "Cuba": [21.521757, -77.781167],
                "Cyprus": [35.126413, 33.429859],
                "Czech Republic": [49.817492, 15.472962],
                "Denmark": [56.26392, 9.501785],
                "Djibouti": [11.825138, 42.590275],
                "Dominica": [15.414999, -61.370976],
                "Dominican Republic": [18.735693, -70.162651],
                "Ecuador": [-1.831239, -78.183406],
                "Egypt": [26.820553, 30.802498],
                "El Salvador": [13.794185, -88.89653],
                "Equatorial Guinea": [1.650801, 10.267895],
                "Eritrea": [15.179384, 39.782334],
                "Estonia": [58.595272, 25.013607],
                "Eswatini (Swaziland)": [-26.522503, 31.465866],
                "Ethiopia": [9.145, 40.489673],
                "Fiji": [-17.713371, 178.065032],
                "Finland": [61.92411, 25.748151],
                "France": [46.603354, 1.888334],
                "Gabon": [-0.803689, 11.609444],
                "Gambia": [13.443182, -15.310139],
                "Georgia": [42.315407, 43.356892],
                "Germany": [51.165691, 10.451526],
                "Ghana": [7.946527, -1.023194],
                "Greece": [39.074208, 21.824312],
                "Grenada": [12.1165, -61.678999],
                "Guatemala": [15.783471, -90.230759],
                "Guinea": [9.945587, -9.696645],
                "Guinea-Bissau": [11.803749, -15.180413],
                "Guyana": [4.860416, -58.93018],
                "Haiti": [18.971187, -72.285215],
                "Honduras": [15.199999, -86.241905],
                "Hungary": [47.162494, 19.503304],
                "Iceland": [64.963051, -19.020835],
                "India": [20.593684, 78.96288],
                "Indonesia": [-0.789275, 113.921327],
                "Iran": [32.427908, 53.688046],
                "Iraq": [33.223191, 43.679291],
                "Ireland": [53.41291, -8.24389],
                "Israel": [31.046051, 34.851612],
                "Italy": [41.87194, 12.56738],
                "Jamaica": [18.109581, -77.297508],
                "Japan": [36.204824, 138.252924],
                "Jordan": [30.585164, 36.238414],
                "Kazakhstan": [48.019573, 66.923684],
                "Kenya": [-1.292066, 36.821946],
                "Kiribati": [-3.370417, -168.734039],
                "Kuwait": [29.31166, 47.481766],
                "Kyrgyzstan": [41.20438, 74.766098],
                "Laos": [19.85627, 102.495496],
                "Latvia": [56.879635, 24.603189],
                "Lebanon": [33.854721, 35.862285],
                "Lesotho": [-29.609988, 28.233608],
                "Liberia": [6.428055, -9.429499],
                "Libya": [26.3351, 17.228331],
                "Liechtenstein": [47.166, 9.555373],
                "Lithuania": [55.169438, 23.881275],
                "Luxembourg": [49.815273, 6.129583],
                "Madagascar": [-18.766947, 46.869107],
                "Malawi": [-13.254308, 34.301525],
                "Malaysia": [4.210484, 101.975766],
                "Maldives": [3.202778, 73.22068],
                "Mali": [17.570692, -3.996166],
                "Malta": [35.937496, 14.375416],
                "Marshall Islands": [7.131474, 171.184478],
                "Mauritania": [21.00789, -10.940835],
                "Mauritius": [-20.348404, 57.552152],
                "Mexico": [23.634501, -102.552784],
                "Moldova": [47.411631, 28.369885],
                "Monaco": [43.738417, 7.424616],
                "Mongolia": [46.862496, 103.846656],
                "Montenegro": [42.708678, 19.37439],
                "Morocco": [31.791702, -7.09262],
                "Mozambique": [-18.665695, 35.529562],
                "Myanmar": [21.913965, 95.956223],
                "Namibia": [-22.95764, 18.49041],
                "Nauru": [-0.522778, 166.931503],
                "Nepal": [28.394857, 84.124008],
                "Netherlands": [52.132633, 5.291266],
                "New Zealand": [-40.900557, 174.885971],
                "Nicaragua": [12.865416, -85.207229],
                "Niger": [17.607789, 8.081666],
                "Nigeria": [9.081999, 8.675277],
                "North Macedonia": [41.608635, 21.745275],
                "Norway": [60.472024, 8.468946],
                "Oman": [21.473533, 55.975413],
                "Pakistan": [30.375321, 69.345116],
                "Palau": [7.51498, 134.58252],
                "Panama": [8.537981, -80.782127],
                "Papua New Guinea": [-6.314993, 143.95555],
                "Paraguay": [-23.442503, -58.443832],
                "Peru": [-9.189967, -75.015152],
                "Philippines": [12.879721, 121.774017],
                "Poland": [51.919438, 19.145136],
                "Portugal": [39.399872, -8.224454],
                "Qatar": [25.354826, 51.183884],
                "Romania": [45.943161, 24.96676],
                "Russia": [61.52401, 105.318756],
                "Rwanda": [-1.940278, 29.873888],
                "Saint Kitts and Nevis": [17.357822, -62.782998],
                "Saint Lucia": [13.909444, -60.978893],
                "Saint Vincent and the Grenadines": [13.252817, -61.197079],
                "Samoa": [-13.759029, -172.104629],
                "San Marino": [43.94236, 12.457777],
                "Sao Tome and Principe": [0.18636, 6.613081],
                "Saudi Arabia": [23.885942, 45.079162],
                "Senegal": [14.497401, -14.452362],
                "Serbia": [44.016521, 21.005859],
                "Seychelles": [-4.679574, 55.491977],
                "Sierra Leone": [8.460555, -11.779889],
                "Singapore": [1.352083, 103.819836],
                "Slovakia": [48.669026, 19.699024],
                "Slovenia": [46.151241, 14.995463],
                "Solomon Islands": [-9.64571, 160.156194],
                "Somalia": [5.152149, 46.199616],
                "South Africa": [-30.559482, 22.937506],
                "South Korea": [35.907757, 127.766922],
                "South Sudan": [7.862684, 30.217636],
                "Spain": [40.463667, -3.74922],
                "Sri Lanka": [7.873054, 80.771797],
                "Sudan": [12.862807, 30.217636],
                "Suriname": [3.919305, -56.027783],
                "Sweden": [60.128161, 18.643501],
                "Switzerland": [46.818188, 8.227512],
                "Syria": [34.802075, 38.996815],
                "Taiwan": [23.69781, 120.960515],
                "Tajikistan": [38.861034, 71.276093],
                "Tanzania": [-6.369028, 34.888822],
                "Thailand": [15.870032, 100.992541],
                "Timor-Leste": [-8.874217, 125.727539],
                "Togo": [8.619543, 0.824782],
                "Tonga": [-21.178986, -175.198242],
                "Trinidad and Tobago": [10.691803, -61.222503],
                "Tunisia": [33.886917, 9.537499],
                "Turkey": [38.963745, 35.243322],
                "Turkmenistan": [38.969719, 59.556278],
                "Tuvalu": [-7.109535, 179.194291],
                "Uganda": [1.373333, 32.290275],
                "Ukraine": [48.379433, 31.16558],
                "United Arab Emirates": [23.424076, 53.847818],
                "United Kingdom": [55.378051, -3.435973],
                "United States": [37.09024, -95.712891],
                "Uruguay": [-32.522779, -55.765835],
                "Uzbekistan": [41.377491, 64.585262],
                "Vanuatu": [-15.376706, 166.959158],
                "Vatican City": [41.902916, 12.453389],
                "Venezuela": [6.42375, -66.58973],
                "Vietnam": [14.058324, 108.277199],
                "Yemen": [15.552727, 48.516388],
                "Zambia": [-13.133897, 27.849332],
                "Zimbabwe": [-19.015438, 29.154857]
            };
            

            filteredData.forEach(item => {
                const country = item["Country name"];
                const latitude = countryCoordinates[country]?.[0];
                const longitude = countryCoordinates[country]?.[1];

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
        })
        .catch(error => console.error('Error loading the JSON data:', error));
}

// Initialize the dropdown and load the initial data
initializeDropdownAndData();
