Project Proposal: Visualizing Global Happiness Trends Using the World Happiness Dataset

1. Project Title:

“Understanding Global Happiness: A Data-Driven Visualization of Happiness Trends”

2. Problem Statement:

Global happiness and well-being have become key indicators for measuring the quality of life in different nations. By examining factors such as income, social support, health, and personal freedoms, governments and organizations can better understand what contributes to happiness. This project aims to leverage the World Happiness Report dataset to identify trends and patterns in happiness levels across different countries, over time, and in relation to key social and economic indicators.

3. Objectives:

	•	To visualize happiness scores and analyze contributing factors across countries.
	•	To provide interactive visualizations that allow users to filter and explore relationships between different variables, such as GDP, life expectancy, and social support.
	•	To include user-driven interactions, such as dropdowns, time-series analysis, and region-based filtering, to offer an engaging exploration of the dataset.

4. Dataset Overview:

	•	Dataset Source: World Happiness Report 2024
	•	Content: This dataset includes happiness scores for over 100 countries and ranks them based on factors such as GDP per capita, social support, life expectancy, freedom to make life choices, and perceptions of corruption.
	•	Size: The dataset consists of over 150 records, including data from multiple years, making it ideal for time-series analysis and cross-country comparisons.

5. Proposed Approach:

	1.	Data Storage and Extraction:
	•	Store the dataset in SQLite for efficient querying and filtering, adhering to the requirement for database extraction.
	2.	Visualization and Interaction:
	•	Libraries Used:
	•	Matplotlib/Seaborn for basic visualizations.
	•	Plotly for interactive and dynamic visualizations (since this library wasn’t covered in class).
	•	Interactive Visualizations:
	•	Global Happiness Map: A heatmap or choropleth map displaying happiness scores across countries.
	•	Time-Series Plots: Visualize trends in happiness over time with interactive filters for specific regions or countries.
	•	Correlation Plot: A scatter plot that allows users to explore the relationships between happiness scores and contributing factors like GDP, social support, or life expectancy.
	3.	User Interaction:
	•	Provide dropdowns for selecting regions, countries, and years.
	•	Allow users to select individual variables (e.g., social support, GDP) and observe their impact on happiness across the world.
	•	Include interactive tooltips that provide more information when users hover over data points or countries on the map.
	4.	Views and Final Visualization:
	•	Create a final dashboard with three distinct views:
	1.	Global Happiness Overview: A global map of happiness scores by country.
	2.	Factor Analysis: Interactive visualizations showing the relationship between happiness and variables like GDP, health, and freedom.
	3.	Yearly Trends: A time-series view tracking happiness changes across different regions and countries.

6. Tools & Technologies:

	•	Database: SQLite (for data storage and querying).
	•	Programming Languages: Python (for data analysis and visualization).
	•	Libraries:
	•	Pandas, NumPy for data manipulation.
	•	Matplotlib, Seaborn for static visualizations.
	•	Plotly for interactive charts and maps.
	•	Flask (Optional): For creating a backend to serve interactive visualizations, if necessary.
	•	Frontend Interaction: HTML and JavaScript for menus and dropdowns to enhance user experience.

7. Expected Outcomes:

	•	A set of interactive visualizations that provide a deep understanding of global happiness patterns and trends.
	•	Insights into which factors contribute most to happiness across different countries and how these have changed over time.
	•	An easy-to-use dashboard where users can explore the data and customize their view to suit their specific interests.

8. Data URL: https://worldhappiness.report/data/

Making a map out of Streamlit
	•	Streamlit is another Python framework for building data science web applications. You can use Python code to build the entire frontend, including buttons, sliders, and visualizations, without needing to know JavaScript, HTML, or CSS.