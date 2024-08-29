import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# NFL color scheme
NFL_COLORS = {
    'primary': '#013369',  # Navy Blue
    'secondary': '#D50A0A',  # Red
    'accent1': '#FFB612',  # Gold
    'accent2': '#4D4D4D',  # Gray
    'background': '#FFFFFF'  # White
}

def plot_injury_type_distribution(df_concussions, height=500, width=700):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Get counts of injury types
    injury_types = df_concussions['Reported Injury Type'].value_counts()

    # Create pie chart
    fig = px.pie(
        values=injury_types.values,
        names=injury_types.index,
        title='Distribution of Reported Injury Types',
        color_discrete_sequence=[NFL_COLORS['primary'], NFL_COLORS['secondary'], NFL_COLORS['accent1'], NFL_COLORS['accent2']]
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Update layout for better readability
    fig.update_layout(
        font=dict(family="Arial", size=12, color=NFL_COLORS['primary']),
        plot_bgcolor=NFL_COLORS['background'],
        paper_bgcolor=NFL_COLORS['background'],
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def plot_injury_severity_by_type(df_concussions, height=500, width=700):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Calculate average recovery time by injury type
    avg_recovery_time = df_concussions.groupby('Reported Injury Type')['Weeks Injured'].mean().sort_values(ascending=True)

    # Create horizontal bar chart
    fig = go.Figure(go.Bar(
        y=avg_recovery_time.index,
        x=avg_recovery_time.values,
        orientation='h',
        marker_color=NFL_COLORS['primary']
    ))

    fig.update_layout(
        title='Average Recovery Time by Injury Type',
        xaxis_title='Average Weeks Injured',
        yaxis_title='Injury Type',
        font=dict(family="Arial", size=12, color=NFL_COLORS['primary']),
        plot_bgcolor=NFL_COLORS['background'],
        paper_bgcolor=NFL_COLORS['background'],
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig

def plot_injury_heatmap(df_concussions, height=600, width=800):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Pivot data to create heatmap
    injury_pivot = df_concussions.pivot_table(
        values='ID',
        index='Position',
        columns='Week of Injury',
        aggfunc='count',
        fill_value=0
    )

    # Create heatmap
    fig = px.imshow(
        injury_pivot,
        title='Injury Heatmap: Position vs. Week of Injury',
        labels=dict(x="Week of Injury", y="Position", color="Number of Injuries"),
        color_continuous_scale=[NFL_COLORS['background'], NFL_COLORS['primary']]
    )

    # Update layout for better readability
    fig.update_layout(
        font=dict(family="Arial", size=12, color=NFL_COLORS['primary']),
        plot_bgcolor=NFL_COLORS['background'],
        paper_bgcolor=NFL_COLORS['background'],
        height=height,
        width=width,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig