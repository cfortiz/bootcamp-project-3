# Understanding Global Happiness: Data-Driven Visualization of Happiness Trends

Global happiness and well-being have become key indicators for measuring the
quality of life in different nations. By examining factors such as income,
social support, health, and personal freedoms, governments and organizations can
better understand what contributes to happiness. This project aims to leverage
the World Happiness Report dataset to identify trends and patterns in happiness
levels across different countries, over time, and in relation to key social and
economic indicators.

## Objectives

* To visualize happiness scores and analyze contributing factors across
  countries.
* To provide interactive visualizations that allow users to filter and explore
  relationships between different variables, such as GDP, life expectancy, and
  social support.
* To include user-driven interactions, such as dropdowns, time-series analysis,
  and region-based filtering, to offer an engaging exploration of the dataset.

## Dataset Overview

* Dataset Source: World Happiness Report 2024
* Content: This dataset includes happiness scores for over 100 countries and
  ranks them based on factors such as GDP per capita, social support, life
  expectancy, freedom to make life choices, and perceptions of corruption.
* Size: The dataset consists of over 150 records, including data from multiple
  years, making it ideal for time-series analysis and cross-country comparisons.

## Proposed Approach

### Data Storage and Extraction

* Store the dataset in SQLite for efficient querying and filtering, adhering to
  the requirement for database extraction.

### Visualization and Interaction

* Libraries Used:

  * Matplotlib/Seaborn for basic visualizations.

  * Plotly for interactive and dynamic visualizations (since this library wasn’t
    covered in class).

* Interactive Visualizations:

  * Global Happiness Map: A heatmap or choropleth map displaying happiness
    scores across countries.

  * Time-Series Plots: Visualize trends in happiness over time with interactive
    filters for specific regions or countries.

  * Correlation Plot: A scatter plot that allows users to explore the
    relationships between happiness scores and contributing factors like GDP,
    social support, or life expectancy.

### User Interaction

* Provide dropdowns for selecting regions, countries, and years.

* Allow users to select individual variables (e.g., social support, GDP) and
  observe their impact on happiness across the world.

* Include interactive tooltips that provide more information when users hover
  over data points or countries on the map.

### Views and Final Visualization

Create a final dashboard with three distinct views:

1. Global Happiness Overview: A global map of happiness scores by country.

1. Factor Analysis: Interactive visualizations showing the relationship between
   happiness and variables like GDP, health, and freedom.

1. Yearly Trends: A time-series view tracking happiness changes across different
   regions and countries.

### Tools & Technologies

* Database
  * MongoDB: for data storage and querying
* Programming Languages
  * Python: for data analysis and visualization
* Libraries
  * Data Manipulation
    * Pandas
    * Numpy
  * Static Visualizations
    * Matplotlib
    * Seaborn
  * Interactive charts and maps
    * Plotly
  * Back-end service for querying
    * Flask
* Front End
  * HTML for layout
  * CSS for styling
  * JavaScript for UI elements

#### Other Tools & Technologies

**Streamlit**: a Python framework for building data science web applications. You
can use Python code to build the entire frontend, including buttons, sliders,
and visualizations, without needing to know JavaScript, HTML, or CSS.

### Expected Outcomes

* A set of interactive visualizations that provide a deep understanding of
  global happiness patterns and trends.
* Insights into which factors contribute most to happiness across different
  countries and how these have changed over time.
* An easy-to-use dashboard where users can explore the data and customize their
  view to suit their specific interests.

### Data Provenance

Our data has been sourced from the _World Happiness Report_, a partnership of
Gallup, the Oxford Wellbeing Research Centre, the UN Sustainable Development
Solutions Network, and the WHR’s Editorial Board. The report is produced under
the editorial control of the WHR Editorial Board.

URL: [https://worldhappiness.report/data/](https://worldhappiness.report/data/)
