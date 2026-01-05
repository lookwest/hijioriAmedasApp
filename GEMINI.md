# GEMINI.md

## Directory Overview

This directory contains a data analysis project focused on the weather data from the Hijiori AMeDAS station in Japan. The project consists of Python scripts for data acquisition, analysis, and visualization, as well as the weather data itself in CSV format.

## Key Files

*   **`hijioriAmedas_data_utf8.csv`**: The primary dataset containing daily weather observations from 1978 to the present.
*   **`update_weather_data.py`**: A Python script to fetch the latest weather data from the Japan Meteorological Agency (JMA) and update the local CSV data.
*   **`analyze_*.py` scripts**: A collection of Python scripts for performing various analyses on the weather data, such as calculating yearly summer statistics, analyzing hot streaks, and comparing precipitation patterns.
*   **`plot_*.py` scripts**: Python scripts that use libraries like `matplotlib` and `pandas` to generate plots and visualizations of the analyzed data.
*   **`*.png` images**: PNG images that are the output of the plotting scripts.
*   **`*.txt` and `*.csv` files (other than the main data file)**: These files contain the output of the analysis scripts.
*   **`start_gemini.sh`**: A shell script that suggests a custom `gemini` tool is used to interact with the data.

## Usage

### Data Update

To update the weather data with the latest observations from the JMA, run the following command:

```bash
python3 update_weather_data.py
```

### Data Analysis

The various Python scripts in the directory can be run to perform specific analyses. For example, to analyze the summer weather for the past 10 years, run:


Similarly, other `analyze_*.py` and `plot_*.py` scripts can be executed to perform other analyses and generate visualizations.

## Language

Future interactions regarding this project will be conducted in Japanese.