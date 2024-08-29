# dashboards/team_analysis.py
import streamlit as st
from src.visualization.team_analysis import plot_team_analysis, plot_team_injury_heatmap, \
    plot_team_injury_trends

def display_team_logo(team_data):
    """Display the team logo or a placeholder if not available."""
    logo_url = team_data['Logo'] if team_data['Logo'] != 'Unknown' else "https://iconerecife.com.br/wp-content/plugins/uix-page-builder/uixpb_templates/images/UixPageBuilderTmpl/no-logo.png"
    st.image(logo_url, width=100)

def team_analysis_dashboard(preprocessed_data):
    """Display the NFL Team Injury Analysis Dashboard."""

    # Import CSS for styling
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Team selector
    teams = preprocessed_data['nfl_teams']['Team'].unique()
    selected_team = st.selectbox("Select a team", teams)

    # Display team-specific metrics
    team_data = preprocessed_data['nfl_teams'][preprocessed_data['nfl_teams']['Team'] == selected_team].iloc[0]

    # Layout: Logo and Team Description
    col1, col2 = st.columns([1, 3])
    with col1:
        display_team_logo(team_data)
    with col2:
        st.markdown(f"### {selected_team}")
        st.markdown(f"*{team_data['Description']}*")

    st.markdown("---")

    # Key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Injuries (2012-2014)", f"{team_data['Total Number of Injuries (2012-2014)']:,}")
    col2.metric("Avg. Injuries per Season", f"{team_data['Total Number of Injuries (2012-2014)'] / 3:.2f}")
    col3.metric("Total Weeks of Injury", f"{team_data['Total Weeks of Injury, by all its players (2012-2014)']:,}")

    st.markdown("---")

    # Team Comparison Chart
    team_comparison_chart = plot_team_analysis(preprocessed_data['nfl_teams'])
    st.plotly_chart(team_comparison_chart, use_container_width=True)

    # Team Injury Heatmap
    team_heatmap = plot_team_injury_heatmap(preprocessed_data['nfl_teams'])
    st.plotly_chart(team_heatmap, use_container_width=True)

    # Replace the existing Team Injury Rates section with this:
    injury_trends_chart = plot_team_injury_trends(preprocessed_data['nfl_teams'])
    st.plotly_chart(injury_trends_chart, use_container_width=True)
