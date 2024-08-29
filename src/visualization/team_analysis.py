# src/visualization/team_analysis.py
import streamlit as st

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

def plot_team_analysis(df_teams, top_n=None, color_scheme=None, title_font_size=16, axis_font_size=14, height=600):
    if not isinstance(df_teams, pd.DataFrame) or df_teams.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    required_columns = ['Team', 'Total Number of Injuries (2012-2014)', 'Total Weeks of Injury, by all its players (2012-2014)']
    if not all(col in df_teams.columns for col in required_columns):
        raise ValueError(f"DataFrame is missing one or more required columns: {required_columns}")

    df_sorted = df_teams.sort_values('Total Number of Injuries (2012-2014)', ascending=False)

    if top_n is not None and isinstance(top_n, int):
        df_sorted = df_sorted.head(top_n)

    # Default color scheme if not provided
    default_colors = {'bar': '#003b6f', 'line': '#d50a0a'}
    colors = color_scheme or default_colors

    fig = go.Figure()

    # Bar for total injuries
    fig.add_trace(go.Bar(
        x=df_sorted['Team'],
        y=df_sorted['Total Number of Injuries (2012-2014)'],
        name='Total Injuries',
        marker_color=colors['bar']
    ))

    # Line for average weeks of injury
    fig.add_trace(go.Scatter(
        x=df_sorted['Team'],
        y=df_sorted['Total Weeks of Injury, by all its players (2012-2014)'] / df_sorted['Total Number of Injuries (2012-2014)'],
        name='Avg. Weeks of Injury',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color=colors['line']),
        marker=dict(color=colors['line'])
    ))

    # Layout adjustments
    fig.update_layout(
        title='NFL Teams: Total Injuries vs Average Injury Duration (2012-2014)',
        xaxis_title='Team',
        yaxis_title='Total Number of Injuries',
        yaxis2=dict(
            title='Average Weeks of Injury',
            overlaying='y',
            side='right'
        ),
        barmode='group',
        hovermode="x unified",
        height=height,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        margin=dict(l=40, r=40, t=40, b=80)
    )

    fig.update_xaxes(tickangle=45)

    return fig

def plot_team_injury_heatmap(df_teams, color_scale='Reds', height=800, title_font_size=16, axis_font_size=14):
    if not isinstance(df_teams, pd.DataFrame) or df_teams.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    seasons = ['2012/2013', '2013/2014', '2014/2015']
    required_columns = ['Team'] + [f'{season} - Number of Injuries' for season in seasons]
    if not all(col in df_teams.columns for col in required_columns):
        raise ValueError(f"DataFrame is missing one or more required columns: {required_columns}")

    injury_data = df_teams[['Team'] + [f'{season} - Number of Injuries' for season in seasons]].set_index('Team')

    fig = px.imshow(
        injury_data,
        labels=dict(x="Season", y="Team", color="Number of Injuries"),
        x=seasons,
        y=injury_data.index,
        aspect="auto",
        title="NFL Team Injuries Heatmap (2012-2015)",
        color_continuous_scale=color_scale
    )

    fig.update_xaxes(side="top")
    fig.update_layout(
        height=height,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        coloraxis_colorbar_title_font=dict(size=axis_font_size, color="#003b6f"),
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_team_injury_rates(df_teams, df_matches, color_scale='Reds', height=600, title_font_size=16, axis_font_size=14):
    if not isinstance(df_teams, pd.DataFrame) or df_teams.empty or not isinstance(df_matches, pd.DataFrame) or df_matches.empty:
        raise ValueError("Both inputs must be non-empty pandas DataFrames")

    # Calculate total games played by each team
    team_games = pd.concat([df_matches['Team 1'], df_matches['Team 2']]).value_counts().reset_index()
    team_games.columns = ['Team', 'Games Played']

    # Merge with injury data
    df_merged = df_teams.merge(team_games, on='Team', how='left')
    df_merged['Injury Rate'] = df_merged['Total Number of Injuries (2012-2014)'] / df_merged['Games Played']

    # Handle cases where 'Games Played' might be 0 or NaN
    df_merged['Injury Rate'] = df_merged['Injury Rate'].fillna(0)

    # Sort by injury rate
    df_sorted = df_merged.sort_values('Injury Rate', ascending=False)

    fig = px.bar(
        df_sorted,
        x='Team',
        y='Injury Rate',
        title='NFL Teams: Injury Rate (2012-2014)',
        labels={'Injury Rate': 'Injuries per Game'},
        color='Injury Rate',
        color_continuous_scale=color_scale,
        height=height
    )

    fig.update_layout(
        xaxis_tickangle=45,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        coloraxis_colorbar_title_font=dict(size=axis_font_size, color="#003b6f"),
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_team_injury_trends(df_teams):
    seasons = ['2012/2013', '2013/2014', '2014/2015']
    df_melt = df_teams.melt(
        id_vars=['Team'],
        value_vars=[f'{season} - Number of Injuries' for season in seasons],
        var_name='Season',
        value_name='Injuries'
    )
    df_melt['Season'] = df_melt['Season'].str.split(' - ').str[0]

    fig = px.bar(
        df_melt,
        x='Team',
        y='Injuries',
        color='Season',
        title='NFL Teams: Injury Trends Across Seasons (2012-2015)',
        labels={'Injuries': 'Number of Injuries'},
        height=600,
        barmode='stack'
    )

    fig.update_layout(
        xaxis_tickangle=45,
        legend_title_text='Season',
        xaxis_title='Team',
        yaxis_title='Number of Injuries',
        hovermode='x unified'
    )

    return fig
