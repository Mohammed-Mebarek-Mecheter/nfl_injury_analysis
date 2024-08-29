# src/visualization/player_analysis.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def plot_player_analysis(df_head_injuries, top_n=20, height=600, width=1000, title_font_size=16, axis_font_size=14):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    df_sorted = df_head_injuries.sort_values('Total Number of Injuries (2012-2014)', ascending=False).head(top_n)

    fig = go.Figure()

    # Bar for total injuries
    fig.add_trace(go.Bar(
        x=df_sorted['Player'],
        y=df_sorted['Total Number of Injuries (2012-2014)'],
        name='Total Injuries',
        marker_color='#003b6f'  # Dark blue
    ))

    # Scatter for games missed, highlighting outliers
    fig.add_trace(go.Scatter(
        x=df_sorted['Player'],
        y=df_sorted['Total Games Missed (2012-2014)'],
        name='Games Missed',
        yaxis='y2',
        mode='markers',
        marker=dict(
            color='#d50a0a',  # Red for games missed
            size=df_sorted['Total Games Missed (2012-2014)'],  # Size based on number of games missed
            sizemode='area',
            sizeref=2.*max(df_sorted['Total Games Missed (2012-2014)'])/(40.**2),
            sizemin=4,
            line=dict(
                color='#003b6f',  # Dark blue for marker border
                width=2
            )
        )
    ))

    fig.update_layout(
        title='Top 20 Players: Total Injuries vs Games Missed (2012-2014)',
        xaxis_title='Player',
        yaxis_title='Total Number of Injuries',
        yaxis2=dict(
            title='Total Games Missed',
            overlaying='y',
            side='right'
        ),
        barmode='group',
        hovermode="x unified",
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=80)
    )

    fig.update_xaxes(tickangle=45)

    return fig

def plot_injury_by_position(df_head_injuries, height=600, width=900, title_font_size=16, axis_font_size=14, sort_ascending=True):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    position_injuries = df_head_injuries.groupby('Roles during injuries')['Total Number of Injuries (2012-2014)'].sum().sort_values(ascending=sort_ascending)

    fig = px.bar(
        x=position_injuries.values,
        y=position_injuries.index,
        orientation='h',
        labels={'x': 'Total Injuries', 'y': 'Position'},
        title='Injury Distribution by Player Position (2012-2014)',
        color=position_injuries.values,
        color_continuous_scale=px.colors.sequential.Blues
    )

    fig.update_layout(
        hovermode="y unified",
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        coloraxis_colorbar_title_font=dict(size=axis_font_size, color="#003b6f"),
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_player_injury_history(df_head_injuries, player_name):
    player_data = df_head_injuries[df_head_injuries['Player'] == player_name].iloc[0]

    seasons = ['2012/2013', '2013/2014', '2014/2015']
    injuries = [player_data[f'{season} - Number of Injuries'] for season in seasons]
    games_missed = [player_data[f'{season} - Games Missed'] for season in seasons]

    fig = go.Figure(data=[
        go.Bar(name='Number of Injuries', x=seasons, y=injuries, marker_color='#003b6f'),
        go.Bar(name='Games Missed', x=seasons, y=games_missed, marker_color='#d50a0a')
    ])

    fig.update_layout(
        title=f'Injury History for {player_name}',
        xaxis_title='Season',
        yaxis_title='Count',
        barmode='group',
        title_font=dict(size=16, color="#003b6f"),
        xaxis_title_font=dict(size=14, color="#003b6f"),
        yaxis_title_font=dict(size=14, color="#003b6f"),
        legend_title_font=dict(size=14, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        height=500,
        width=800
    )

    return fig

def plot_player_injury_history(df_head_injuries, player_name, height=500, width=800, title_font_size=16, axis_font_size=14):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    player_data = df_head_injuries[df_head_injuries['Player'] == player_name]
    if player_data.empty:
        raise ValueError(f"No data found for player: {player_name}")

    player_data = player_data.iloc[0]
    seasons = ['2012/2013', '2013/2014', '2014/2015']
    injuries = [player_data[f'{season} - Number of Injuries'] for season in seasons]
    games_missed = [player_data[f'{season} - Games Missed'] for season in seasons]

    fig = go.Figure(data=[
        go.Bar(name='Number of Injuries', x=seasons, y=injuries, marker_color='#003b6f'),
        go.Bar(name='Games Missed', x=seasons, y=games_missed, marker_color='#d50a0a')
    ])

    fig.update_layout(
        title=f'Injury History for {player_name}',
        xaxis_title='Season',
        yaxis_title='Count',
        barmode='group',
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_age_vs_injuries(df_head_injuries, height=600, width=1000, title_font_size=16, axis_font_size=14):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    fig = px.scatter(
        df_head_injuries,
        x='Age first concussion (2012-2014)',
        y='Total Number of Injuries (2012-2014)',
        color='Roles during injuries',
        size='Total Games Missed (2012-2014)',
        hover_data=['Player', 'Team(s) during concussion incidents 2012-2014'],
        title='Age at First Concussion vs. Total Number of Injuries',
        labels={
            'Age first concussion (2012-2014)': 'Age at First Concussion',
            'Total Number of Injuries (2012-2014)': 'Total Number of Injuries',
            'Roles during injuries': 'Position'
        }
    )

    fig.update_layout(
        height=height,
        width=width,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_injury_severity_distribution(df_head_injuries, height=500, width=700, title_font_size=16, legend_font_size=12, color_scheme=None):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    # Define severity categories
    df_head_injuries['Injury Severity'] = pd.cut(
        df_head_injuries['Total Games Missed (2012-2014)'],
        bins=[0, 1, 3, 6, np.inf],
        labels=['Minor (0-1)', 'Moderate (2-3)', 'Severe (4-6)', 'Very Severe (7+)']
    )

    severity_counts = df_head_injuries['Injury Severity'].value_counts().sort_index()

    # Use a default color scheme if none is provided
    colors = color_scheme or px.colors.sequential.Blues_r

    fig = px.pie(
        values=severity_counts.values,
        names=severity_counts.index,
        title='Distribution of Injury Severity (2012-2014)',
        color_discrete_sequence=colors
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_font=dict(size=title_font_size, color="#003b6f"),
        legend_title_font=dict(size=legend_font_size, color="#003b6f"),
        legend_font=dict(size=legend_font_size, color="#003b6f"),
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig

def plot_injury_trend_over_seasons(df_head_injuries, height=500, width=800, title_font_size=16, axis_font_size=14):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("Input must be a non-empty pandas DataFrame")

    seasons = ['2012/2013', '2013/2014', '2014/2015']
    injuries_by_season = [df_head_injuries[f'{season} - Number of Injuries'].sum() for season in seasons]
    games_missed_by_season = [df_head_injuries[f'{season} - Games Missed'].sum() for season in seasons]

    fig = go.Figure(data=[
        go.Bar(name='Number of Injuries', x=seasons, y=injuries_by_season, marker_color='#003b6f'),
        go.Bar(name='Games Missed', x=seasons, y=games_missed_by_season, marker_color='#d50a0a')
    ])

    fig.update_layout(
        title='Injury Trend Over Seasons',
        xaxis_title='Season',
        yaxis_title='Count',
        barmode='group',
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_title_font=dict(size=axis_font_size, color="#003b6f"),
        legend_font=dict(size=12, color="#003b6f"),
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=80)
    )

    return fig
