import pandas as pd
import streamlit as st
import plotly.express as px
from src.utils.helpers import calculate_injury_rate

def seasonal_trends_dashboard(preprocessed_data):
    # Load season data
    df_seasons = preprocessed_data['seasons']

    # Import CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Seasonal Trends Analysis")

    # Season selector at the top of the page
    all_seasons = df_seasons['Season'].unique()
    selected_season = st.selectbox(
        "Select a Season",
        options=all_seasons
    )

    # Filter data based on selected season
    filtered_seasons = df_seasons[df_seasons['Season'] == selected_season]

    # Display season-specific metrics
    season_data = filtered_seasons.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Injuries", f"{season_data['Total Number of Injuries']:,}")
    col2.metric("Total Games Missed", f"{season_data['Total Games Missed, by all players']:,}")
    col3.metric("Avg. Weeks of Injury", f"{season_data['Total Weeks of Injury, all its players'] / season_data['Total Number of Injuries']:.2f}")

    st.markdown("---")

    # Injury trend throughout the season
    col1, col2 = st.columns(2)
    with col1:
        season_injuries = preprocessed_data['concussions'][preprocessed_data['concussions']['Season'] == selected_season]
        weekly_injuries = season_injuries.groupby('Week of Injury')['ID'].count().reset_index(name='Injury Count')
        fig = px.line(weekly_injuries, x='Week of Injury', y='Injury Count',
                      title=f"Weekly Injury Trend - {selected_season}",
                      line_shape='linear',
                      color_discrete_sequence=['#0033A0'])  # Dark Blue
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        injury_types = season_injuries['Reported Injury Type'].value_counts()
        fig = px.pie(values=injury_types.values, names=injury_types.index,
                     title=f"Injury Types Distribution - {selected_season}",
                     hole=0.3,  # Donut chart style
                     color_discrete_sequence=['#0033A0', '#E03A3E', '#27AE60', '#F39C12'])  # Dark Blue, Red, Green, Orange
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Comparison of pre-season vs regular season injuries
    col1, col2 = st.columns(2)
    with col1:
        preseason_injuries = season_injuries[season_injuries['Pre-Season Injury?'] == 'Yes'].shape[0]
        regular_season_injuries = season_injuries[season_injuries['Pre-Season Injury?'] == 'No'].shape[0]
        fig = px.bar(x=['Pre-Season', 'Regular Season'], y=[preseason_injuries, regular_season_injuries],
                     title=f"Pre-Season vs Regular Season Injuries - {selected_season}",
                     color_discrete_sequence=['#0033A0', '#E03A3E'])  # Dark Blue, Red
        fig.update_layout(
            xaxis_title='Season',
            yaxis_title='Number of Injuries'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        filtered_seasons['Injury Rate'] = filtered_seasons.apply(lambda row: calculate_injury_rate(row['Total Number of Injuries'], row['Total Games Missed, by all players']), axis=1)
        fig = px.bar(filtered_seasons, x='Season', y='Injury Rate',
                     title="Injury Rate Comparison Across Selected Seasons",
                     color_discrete_sequence=['#0033A0', '#E03A3E'])  # Dark Blue, Red
        st.plotly_chart(fig, use_container_width=True)
