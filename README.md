# Data Analytics Boot Camp - Project 3

Understanding Global Happiness

## Members

* Kassidy MunnMinoda
* Kiki Chan
* Elizabeth Conn
* Elif Celebi
* Carlos Ortiz

## Track

This project falls along the Data Visualization track for Project 3.

## Objective

The World Happiness Report aims to assess and rank countries based on
the  well-being and happiness of their citizens. It seeks to influence
policymakers by highlighting the importance of happiness and well-being
in societal development, encouraging efforts to improve the quality of
life for all individuals.

The primary objective of this data visualization project is to provide
insightful, interactive visual representations of happiness level across
various demographics using a detailed dataset. The aim is to highlight
patterns and correlations between happiness level and various indicators
such as income, social support, life expectancy, freedom to make life
choices, generosity, and perceptions of corruption.

## Goals

* To create visualizations revealing patterns in happiness level across
  different demographics.
* To utilize interactive elements to enhance user experience and
  facilitate exploration of the data.
* To use a Python or JavaScript visualization library not previously
  covered in class for innovative data representation.
* To extract and analyze data stored in a database.

## Dataset Overview

Attribution: This project uses data from the
[World Happiness Report Appendices & Data](https://worldhappiness.report/data/).

Please see provided documentation PDF for data spec.

The dataset contains mre than 2500 records, with the following variables
providing a comprehensive view of happiness level:

* **Life Ladder:** A subjective measure where individuals rate
  their current lives on a scale from 0 to 10, reflecting personal
  life satisfaction and well-being.
* **GDP per capita:** Measures the average income per capita,
  reflecting the economic resources available to individuals.
* **Social support:** Assesses the presence of supportive relationships
  and community ties that individuals can rely on in times of need. 
* **Healthy life expectancy at birth:** Indicates the average number
  of years people can expect to live in good health, reflecting overall
  health and healthcare quality.
* **Freedom to make life choices:** Evaluates the extent to which individuals
  feel they have the autonomy to make choices about their own lives.
* **Generosity:** Looks at the level of charitable donations and volunteerism,
  reflecting a society’s willingness to help others.
* **Perceptions of corruption:** Measures how corrupt people perceive their
  government and business sectors, influencing trust and societal well-being.
* **Positive affect:** Measure of laugh, enjoyment, and doing interesting things.
* **Negative affect:** Measure of worry, sadness, and anger.

## Prerequisites

This project requires MongoDB as well as several python libraries.

### Services

* MongoDB running on port 27017

### Python libraries

The following python libraries must be installed via either `pip install` or
`conda install`:

* Jupyter notebooks/lab: `jupyter`
* PyMongo: `pymongo`
* Folium: `folium`
* Numpy: `numpy`
* Pandas: `pandas`
* Plotly: `plotly`
* Streamlit: `streamlit`
* Folium: `folium`
* Steamlit-Folium plugin: `streamlit-folium`

### Data

The mongo database must be imported after MongoDB has been installed, is running
on port 27017, and all python libraries are installed: particularly pymongo.

To import the data, activate your python environment with the prerequisite
libraries, and run the following command from the project's root directory:

`python importdata.py`

This should create a mongo database called 'worldHappiness' with the collections
'fig' and 'table'.

## Running

There are 4 visualizations in this project: 2 html/css/js visualizations using
Leaflet, 1 jupyter notebook, and 1 streamlit interactive visualization.  Please
mare sure all project pre-requisites have been fulfilled before you run these
visualizations to prevent errors.

### Leaflet

To run the leaflet code, change directory to `front_end` and run
`python -m http.server`.  Then access either of the links on your browser:

* [Javascript Mapping](http://localhost:8000/javascript_mapping.html)
* [Time Series Map](http://localhost:8000/time_series_map.html)

Press CTRL-C on the console (might require repeated pressing) to stop the
python http server.

### Streamlit

To run the Streamlit dashboard, first run the following from the project's root
directory:

`streamlit run world-happiness-map.py`

This should open a browser window or tab accessing the dashboard.  If not,
please follow the instructions given by the command's output to access the
dashboard.

Press CTRL-C on the console (might require repeated pressing) to stop the
streamlit application.

### Jupyter Notebook

To run the statistical analysis jupyter notebook, you may run either
`jupyter notebook` or `jupyter lab` from the project's root directory.  This
should open a browser interface from which you can open
'statistical_analysis.ipynb' to review the notebook.

## Files

### Primary files

* `front_end/javascript_mapping.html`: Javascript Mapping HTML visualization
  file.
* `front_end/static/js/javascript_mapping.js`: Static JS code for the Javascript
  Mapping visualization.
* `front_end/static/css/style.css`: Static CSS stylesheet used for Javascript
  Mapping visualization.
* `front_end/time_series_map.html`: Time Series Map HTML visualization file.
* `front_end/static/js/time_series_map.js`: Static JS code for the Time Series
  Map visualization.
* `statistical_analysis.ipynb`: Jupyter Notebook with statistical analysis
  visualizations.
* `world-happiness-map.py`: Streamlit interactive visualization script.
* `Project 3 Presentation.pptx`: Powerpoint presentation file used for the
  presentation on 2024-10-24 during class.
* `project-outline.md`: Markdown outline of the project we used to prepare for
  our work.
* `README.md`: This file.

### Secondary files

* `back_end/resources/countries.geo.json`: GeoJSON file of country boundaries
  for maps.
* `back_end/resources/country_coordinates.csv`: Latitude and longitude
  coordinates for each country as a CSV file.
* `front_end/worldHappiness.table.json`: MongoDB dump of the WHR table data (
  time series data).

### Data source files

The following files were obtained from the
[World Happiness Report](https://worldhappiness.report/) site.  Excel files
obtained from that site were converted to CSV to simplify the data import
process.

* `docs/World Happiness Report 2024 - Appendix.pdf`: This is the documentation
  provided by the World Happiness Report which documents each variable in the
  dataset.
* `resources/world-happiness-fig-2024.csv`: 2024 World Happiness Report data
  (for year 2023) as a CSV file.  Converted to CSV from
  [World Happiness Report 2024 - Data for Figure 2.1](https://happiness-report.s3.amazonaws.com/2024/DataForFigure2.1+with+sub+bars+2024.xls)
  excel file.
* `resources/world-happiness-table-2024.csv`: 2024 World Happiness Report data
  (for years 2005 - 2023) as a CSV file.  Converted to CSV from
  [World Happiness Report 2024 - Data for Table 2.1](https://happiness-report.s3.amazonaws.com/2024/DataForTable2.1.xls)
  excel file.

## Visualizations

### JavaScript Mapping

This is a Leaflet visualization that allows the user to visualize each variable
in the dataset by year randing from 2005 to 2023 through an interactive map.

### Time Series Map

This is a Leaflet visualization that allows the user to visualize the happiness
(a.k.a. ladder) variable from 2008 - 2023 through an animated world map.

### Statistical Analysis

This is a Jupyter Notebook that visualizes a few things:

* Freedom to Make Life Choices vs Perception of Corruption as a scatter plot
* Happiness (Life Ladder) vs Healthy Life Expectancy at Birth as a bubble chart,
  with the size of each bubble scaled by Freedom to Make Life Choices.
* Variable correlation Heat Map: a graded (1.0 green - -1.0 red) heat map of the
  correlation of each variable against other variables.
* Life Ladder vs Log GDP Per Capita as a scatter plot with regression line.
* Top and Bottom countries by Average Life Ladder (happiness metric) for the
  2024 report (2023 data) as bar charts for the top 10 and bottom 10 countries.

### Streamlit Interactive Dashboard

Streamlit python framework dashboard with two tabs.

The "2024 World Map" tab portrays a visualization of the 2024 variable values by
country (interactive) as well as a color-graded heat-map of the happiness metric
for the entire world by country for year 2024.

The "Compare Countries by Year" tab is an interactive visualization of the time
series data for any variable and chosen year range for the country selected in
the "2024 World Map" tab.  This allows the user to select a country in the
"2024 World Map" tab, and then drill down to compare the time series values of
any of the variables, instead of a static view for year 2024.
