# NFL Injury Analysis Dashboard

This project is a comprehensive dashboard for analyzing NFL player injuries from 2012 to 2015. It was developed as part of the Data in Motion Monthly Data Visualization Challenge. The dashboard leverages data on concussion injuries, head injuries, and team performances, providing valuable insights into injury trends, severity, and their impact on players and teams.

## Project Structure

```
nfl_injury_analysis/
├── .streamlit/
│   ├── config.toml                      # Streamlit configuration file
├── app.py                               # Main application entry point
├── dashboards/                          # Directory containing dashboard files
│   ├── player_analysis.py               # Player analysis dashboard
│   ├── seasonal_trends.py               # Seasonal trends analysis dashboard
│   ├── team_analysis.py                 # Team analysis dashboard
├── data/                                # Directory containing dataset files
│   ├── Concussion_Injuries_2012_2014.csv# Concussion injuries data
│   ├── Head_Injured_Players.csv         # Head injured players data
│   ├── Matches_2012_2015.csv            # Match data from 2012 to 2015
│   ├── Match_Dates.csv                  # Match dates and injury count
│   ├── NFL_Teams.csv                    # NFL teams and their injury data
│   ├── Seasons.csv                      # Seasonal injury statistics
├── README.md                            # Project documentation
├── requirements.txt                     # Python package dependencies
├── src/                                 # Source directory for processing and visualization code
│   ├── data_processing/
│   │   ├── load_data.py                 # Functions to load datasets
│   │   ├── preprocess_data.py           # Functions to preprocess datasets
│   │   ├── __init__.py                  # Init file for data_processing module
│   ├── utils/
│   │   ├── helpers.py                   # Utility functions for calculations and formatting
│   │   ├── __init__.py                  # Init file for utils module
│   ├── visualization/
│   │   ├── dashboard_visuals.py         # Common visual components for dashboards
│   │   ├── injury_trends.py             # Injury trend visualizations
│   │   ├── player_analysis.py           # Player-specific visualizations
│   │   ├── team_analysis.py             # Team-specific visualizations
│   │   ├── __init__.py                  # Init file for visualization module
├── style.css                            # Custom CSS for styling the dashboard
```

## Challenge Overview

This project was developed as part of the Data in Motion Monthly Data Visualization Challenge. The challenge required participants to create an insightful data visualization or dashboard using provided datasets. The focus was on exploring NFL injuries to uncover patterns and insights that could be useful for teams, players, and fans.

- **Challenge Source:** [Data in Motion Monthly Data Visualization Challenges](https://datainmotion.co/path-player?courseid=monthly-data-visualization-challenges&unit=66ce80f5e7bcd463f00832bfUnit)
- **Objective:** Analyze NFL injury data from 2012-2014 to provide insights into injury trends, severity, and their impact on players and teams.

## Data Sources

The datasets used in this project cover various aspects of NFL injuries, including:

- **Concussion Injuries 2012-2014:** Detailed data on concussion injuries sustained by NFL players.
- **Head Injured Players:** Data on NFL players who sustained head injuries between 2012 and 2014, including the number of injuries, games missed, and player demographics.
- **Match Dates:** Records of match dates along with the number of injuries, week of the season, and season year.
- **Matches 2012-2015:** Information on 791 football matches from the 2012 to 2015 seasons.
- **NFL Teams:** Data on NFL teams, including the total number of injuries, weeks of injury, and team descriptions.
- **Seasons:** Injury statistics for multiple sports seasons, detailing the total number of injuries, games missed, and weeks of injury for all players.

## Features

### 1. **Team Analysis Dashboard**
- **Total Injuries:** Displays the total number of injuries per team from 2012-2014.
- **Average Injuries per Season:** Provides a breakdown of average injuries per season.
- **Weeks of Injury:** Highlights the total weeks of injury suffered by players in each team.
- **Injury Maps and Charts:** Includes choropleth maps, heatmaps, and injury rate comparisons for teams.

### 2. **Player Analysis Dashboard**
- **Injury Trends by Player:** Shows the top 20 players by the number of injuries and games missed.
- **Injury by Position:** Visualizes the distribution of injuries by player position.
- **Player-Specific Analysis:** Provides detailed insights into the injury history of specific players.

### 3. **Seasonal Trends Dashboard**
- **Injury Trends Over Time:** Line charts showing injury trends across different seasons.
- **Injury Distribution by Season:** Donut charts and bar charts to compare injury distributions across seasons.
- **Injury Severity:** Analyzes the severity of injuries across seasons, highlighting high-risk periods.

## How to Run the Project

### Prerequisites

Ensure you have Python 3.11 or higher installed. You'll also need to install the required Python packages, which are listed in the `requirements.txt` file.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Mohammed-Mebarek-Mecheter/nfl_injury_analysis.git
   cd nfl_injury_analysis
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   ```bash
   streamlit run app.py
   ```

   This command will start a local Streamlit server. Open the provided URL in your web browser to interact with the dashboard.

## Usage

- **Explore Teams:** Select a team from the dropdown menu to view detailed injury statistics, including total injuries, average injuries per season, and weeks of injury.
- **Analyze Players:** Dive into individual player data to see who is most affected by injuries and how it impacts their career.
- **Discover Trends:** Use the seasonal trends dashboard to identify patterns in injury occurrences across different seasons.
- **Advanced Analytics:** Apply machine learning models to predict future injuries or explore the PCA analysis for deeper insights into player injuries.

## Customization

- **Add New Visualizations:** You can extend the dashboard by adding new visualizations in the `src/visualization` directory and integrating them into the respective dashboards.
- **Update Datasets:** To analyze more recent data, update the CSV files in the `data` directory and adjust the data processing scripts as needed.

## Contribution

Contributions are welcome! If you have ideas for new features or enhancements, feel free to fork the repository and submit a pull request.

## Acknowledgments

- **Data in Motion:** Special thanks to Data in Motion for providing the challenge and the datasets. This project was inspired by their Monthly Data Visualization Challenge.
- **NFL Data:** The datasets used in this project are based on NFL injury data, which provide valuable insights into the impact of injuries on the sport.
