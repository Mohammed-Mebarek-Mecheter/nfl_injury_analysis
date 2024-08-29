# src/visualization/advanced_analytics.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def plot_injury_prediction(df_concussions, prediction_model, height=600, width=800, title_font_size=16, axis_font_size=14):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    features = ['Position', 'Pre-Season Injury?', 'Week of Injury', 'Total Snaps']
    X = pd.get_dummies(df_concussions[features], columns=['Position', 'Pre-Season Injury?'])

    probabilities = prediction_model.predict_proba(X)[:, 1]  # Probability of severe injury

    fig = px.scatter(
        df_concussions,
        x='Total Snaps',
        y='Week of Injury',
        color=probabilities,
        hover_data=['Player', 'Position'],
        title='Injury Severity Prediction',
        labels={'color': 'Probability of Severe Injury'}
    )

    fig.update_layout(
        height=height,
        width=width,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig

def plot_pca_analysis(df_head_injuries, height=600, width=800, title_font_size=16, axis_font_size=14):
    if not isinstance(df_head_injuries, pd.DataFrame) or df_head_injuries.empty:
        raise ValueError("df_head_injuries must be a non-empty pandas DataFrame")

    features = ['Total Number of Injuries (2012-2014)', 'Total Games Missed (2012-2014)', 'Age first concussion (2012-2014)']
    X = df_head_injuries[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)

    df_pca = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
    df_pca['Player'] = df_head_injuries['Player']
    df_pca['Position'] = df_head_injuries['Roles during injuries']

    fig = px.scatter(
        df_pca,
        x='PC1',
        y='PC2',
        color='Position',
        hover_data=['Player'],
        title='PCA of Player Injury Data'
    )

    fig.update_layout(
        height=height,
        width=width,
        title_font=dict(size=title_font_size, color="#003b6f"),
        xaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        yaxis_title_font=dict(size=axis_font_size, color="#003b6f"),
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig

def plot_injury_network(df_concussions, height=600, width=800, title_font_size=16, font_size=10):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    injury_connections = df_concussions.groupby(['Position', 'Reported Injury Type']).size().reset_index(name='count')

    positions = list(injury_connections['Position'].unique())
    injury_types = list(injury_connections['Reported Injury Type'].unique())

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=positions + injury_types,
            color="blue"
        ),
        link=dict(
            source=[positions.index(x) for x in injury_connections['Position']],
            target=[len(positions) + injury_types.index(x) for x in injury_connections['Reported Injury Type']],
            value=injury_connections['count']
        )
    )])

    fig.update_layout(
        title_text="Injury Network: Position to Injury Type",
        font_size=font_size,
        title_font=dict(size=title_font_size, color="#003b6f"),
        height=height,
        width=width,
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig