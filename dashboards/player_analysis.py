# dashboards/player_analysis.py
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.visualization.player_analysis import plot_player_analysis, plot_injury_by_position, plot_age_vs_injuries
from src.utils.helpers import format_number

def player_analysis_dashboard(preprocessed_data):

    # Import CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Player selector
    players = preprocessed_data['head_injuries']['Player'].unique()
    selected_player = st.selectbox("Select a player", players)

    # Display player-specific metrics and image
    player_data = preprocessed_data['head_injuries'][preprocessed_data['head_injuries']['Player'] == selected_player].iloc[0]

    col1, col2 = st.columns([1, 3])
    with col1:
        if player_data['Image'] != 'Unknown':
            st.image(player_data['Image'], width=150, caption=player_data['Player'])
        else:
            st.image("https://via.placeholder.com/200x200?text=No+Image", width=150, caption=player_data['Player'])
    with col2:
        st.subheader(selected_player)
        st.write(f"**Position:** {player_data['Roles during injuries']}")
        st.write(f"**Teams:** {player_data['Team(s) during concussion incidents 2012-2014']}")
        st.write(player_data['Biography'])

    # Player metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Injuries (2012-2014)", format_number(player_data['Total Number of Injuries (2012-2014)']))
    with col2:
        st.metric("Total Games Missed", format_number(player_data['Total Games Missed (2012-2014)']))
    with col3:
        st.metric("Age at First Concussion", f"{player_data['Age first concussion (2012-2014)']:.1f}")
    with col4:
        st.metric("Current Age (approx.)", player_data['Current Age (approx.)'])

    # Player injury history
    player_injuries = preprocessed_data['concussions'][preprocessed_data['concussions']['Player'] == selected_player]
    # Aggregate statistics
    # Calculate total injuries
    total_injuries = player_injuries.shape[0]
    # Calculate total games missed
    total_games_missed = player_injuries['Games Missed'].sum()
    # Round the total games missed for practicality
    total_games_missed = round(total_games_missed, 1)
    # Handle average injury duration calculation
    if total_injuries > 1:
        # Ensure 'Date' is in datetime format
        player_injuries['Date'] = pd.to_datetime(player_injuries['Date'])
        # Calculate the duration between injuries (if possible)
        player_injuries.sort_values('Date', inplace=True)
        player_injuries['Duration'] = player_injuries['Date'].diff().dt.days
        # Average duration, excluding NaT (which means only one injury)
        average_injury_duration = player_injuries['Duration'].mean()
    else:
        average_injury_duration = None
    # Display statistics
    st.write(f"Total Injuries: {total_injuries}")
    st.write(f"Total Games Missed: {total_games_missed}")
    st.write(f"Average Injury Duration: {average_injury_duration if average_injury_duration is not None else 'Not Applicable'}")
    # Optionally, visualize
    fig = px.bar(x=['Total Injuries', 'Total Games Missed'], y=[total_injuries, total_games_missed],
                 labels={'x': 'Statistic', 'y': 'Value'},
                 title=f"{selected_player} Injury Statistics")
    st.plotly_chart(fig, use_container_width=True)

    age_vs_injuries_chart = plot_age_vs_injuries(preprocessed_data['head_injuries'])
    st.plotly_chart(age_vs_injuries_chart, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        top_players_chart = plot_player_analysis(preprocessed_data['head_injuries'])
        st.plotly_chart(top_players_chart, use_container_width=True)
    with col2:
        position_chart = plot_injury_by_position(preprocessed_data['head_injuries'])
        st.plotly_chart(position_chart, use_container_width=True)

    # Player comparison
    st.markdown("---")
    players_to_compare = st.multiselect("Select players to compare", players, default=[selected_player])
    if len(players_to_compare) > 1:
        comparison_data = preprocessed_data['head_injuries'][preprocessed_data['head_injuries']['Player'].isin(players_to_compare)]
        comparison_fig = go.Figure()
        for metric in ['Total Number of Injuries (2012-2014)', 'Total Games Missed (2012-2014)', 'Age first concussion (2012-2014)']:
            if metric in comparison_data.columns:
                comparison_fig.add_trace(go.Bar(
                    x=comparison_data['Player'],
                    y=comparison_data[metric],
                    name=metric
                ))
        comparison_fig.update_layout(
            title="Player Comparison",
            xaxis_title="Player",
            yaxis_title="Value",
            barmode='group',
            template='plotly_white'
        )
        st.plotly_chart(comparison_fig, use_container_width=True)

    # About section
    with st.expander('About', expanded=True):
        st.write('''
            - :orange[**Player Comparison**]: Tool to compare injury statistics between multiple players
            ''')
