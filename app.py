import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from src.data_processing import load_all_datasets, preprocess_data
from src.visualization.dashboard_visuals import make_choropleth
from src.visualization.injury_trends import plot_injury_type_distribution, plot_injury_severity_by_type, plot_injury_heatmap
from src.utils.helpers import format_number
from dashboards.team_analysis import team_analysis_dashboard
from dashboards.player_analysis import player_analysis_dashboard
from dashboards.seasonal_trends import seasonal_trends_dashboard
from streamlit_lottie import st_lottie
import json

# Page configuration
st.set_page_config(
    page_title="NFL Injury Analysis Dashboard",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import CSS for styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    datasets = load_all_datasets()
    return preprocess_data(datasets)

preprocessed_data = load_data()

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Overview", "Team Analysis", "Player Analysis", "Seasonal Trends"],
        icons=["house", "shield", "person", "calendar"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "#636161", "font-size": "22px"},
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#013369"},
        }
    )

    # selected_seasons = st.multiselect(
    #     "Select Seasons",
    #     options=preprocessed_data['seasons']['Season'].unique(),
    #     default=preprocessed_data['seasons']['Season'].unique()
    # )

# Function to display key metrics
def display_metrics():
    col1, col2, col3 = st.columns(3)
    total_injuries = preprocessed_data['concussions']['ID'].count()
    total_players = preprocessed_data['head_injuries']['Player'].nunique()
    avg_games_missed = preprocessed_data['head_injuries']['Total Games Missed (2012-2014)'].mean()

    col1.metric("Total Injuries", format_number(total_injuries))
    col2.metric("Players Affected", format_number(total_players))
    col3.metric("Avg. Games Missed", f"{avg_games_missed:.1f}")

# Overview section
if selected == "Overview":
    st.title("NFL Injury Analysis")
    st.markdown("This dashboard provides insights into NFL injuries from 2012 to 2015.")
    display_metrics()

    # Team Injury Map
    choropleth_fig = make_choropleth(preprocessed_data['nfl_teams'], 'Total Number of Injuries (2012-2014)', 'Reds')
    st.plotly_chart(choropleth_fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        injury_type_chart = plot_injury_type_distribution(preprocessed_data['concussions'])
        st.plotly_chart(injury_type_chart, use_container_width=True)

    with col2:
        injury_severity_chart = plot_injury_severity_by_type(preprocessed_data['concussions'])
        st.plotly_chart(injury_severity_chart, use_container_width=True)

    injury_heatmap_chart = plot_injury_heatmap(preprocessed_data['concussions'])
    st.plotly_chart(injury_heatmap_chart, use_container_width=True)

    # About section
    with st.expander('About this NFL Injury Analysis', expanded=False):
        st.write('''
    This NFL Injury Analysis Dashboard offers a deep dive into the injury patterns and trends across the league from 2012 to 2015. The dashboard includes:

    - **Team Performance Insights:** Explore injury data for each NFL team, including total injuries, average injuries per season, and weeks of injury. Compare teams to identify which ones were most affected by injuries.
    - **Player Injury Analysis:** Delve into individual player statistics, examining their injury history, the severity of injuries, and the impact on their playing time. Compare players to understand how injuries vary across positions and careers.
    - **League-Wide Injury Trends:** Analyze how injuries are distributed across the league, with visualizations breaking down injuries by player position, age, and season. Uncover patterns that can inform player safety measures.
    
    The data used in this dashboard is sourced from [Data in Motion](https://datainmotion.co/path-player?courseid=monthly-data-visualization-challenges&unit=66ce80f5e7bcd463f00832bfUnit) It relates to one of their Monthly Data Visualization Challenges. The data has been carefully processed to ensure accuracy and completeness, offering reliable insights into the health and safety of NFL players.
    ''')

# Team Analysis dashboard
elif selected == "Team Analysis":
    team_analysis_dashboard(preprocessed_data)

# Player Analysis dashboard
elif selected == "Player Analysis":
    player_analysis_dashboard(preprocessed_data)

# Seasonal Trends dashboard
elif selected == "Seasonal Trends":
    seasonal_trends_dashboard(preprocessed_data)

# Download button for the full dataset
if st.sidebar.button("Download Full Dataset"):
    @st.cache_data
    def get_full_data():
        return pd.concat([df for df in preprocessed_data.values()], axis=1)

    full_data = get_full_data()
    csv = full_data.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="nfl_injury_analysis_full_dataset.csv",
        mime="text/csv"
    )
# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by **Mebarek**")
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Load Lottie animations
lottie_github = load_lottie_file("assets/images/github.json")
lottie_linkedin = load_lottie_file("assets/images/linkedin.json")
lottie_portfolio = load_lottie_file("assets/images/profile.json")

# Sidebar section with Lottie animations and links
with st.sidebar:
    st.markdown("### Connect with me")

    col1, col2 = st.columns([1, 3])
    with col1:
        st_lottie(lottie_github, height=30, width=30, key="lottie_github_sidebar")
    with col2:
        st.markdown("<a href='https://github.com/Mohammed-Mebarek-Mecheter/' target='_blank'>GitHub</a>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st_lottie(lottie_linkedin, height=30, width=30, key="lottie_linkedin_sidebar")
    with col2:
        st.markdown("<a href='https://www.linkedin.com/in/mohammed-mecheter/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        st_lottie(lottie_portfolio, height=30, width=30, key="lottie_portfolio_sidebar")
    with col2:
        st.markdown("<a href='https://mebarek.pages.dev/' target='_blank'>Portfolio</a>", unsafe_allow_html=True)