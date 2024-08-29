# src/visualization/dashboard_visuals.py
import pandas as pd
import plotly.express as px
import altair as alt
import re
import json

def make_choropleth(df_teams, column, color_theme):
    # Mapping of full state names to state abbreviations
    state_name_to_abbreviation = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
        'District of Columbia': 'DC'
    }

    # Function to extract the state abbreviation using the mapping
    def extract_state_abbreviation(location):
        city, state_name = location.split(", ")
        return state_name_to_abbreviation.get(state_name)

    # Apply the function to get state abbreviations
    df_teams['State'] = df_teams['Location'].apply(extract_state_abbreviation)

    if df_teams['State'].isnull().any():
        missing_states = df_teams[df_teams['State'].isnull()]['Team'].tolist()
        raise ValueError(f"Could not extract state information for teams: {missing_states}")

    # Create the choropleth map using state abbreviations
    choropleth = px.choropleth(
        df_teams,
        locations='State',
        locationmode="USA-states",
        color=column,
        color_continuous_scale=color_theme,
        scope="usa",
        labels={column: column.replace('_', ' ').title()}
    )

    choropleth.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )

    return choropleth

def format_number(num):
    if num >= 1000000:
        return f'{num // 1000000}M'
    elif num >= 1000:
        return f'{num // 1000}K'
    else:
        return str(num)

def calculate_injury_difference(df_concussions, year):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Extract starting year for comparison
    df_concussions['Season_Start'] = df_concussions['Season'].apply(lambda x: int(x.split('/')[0]))

    # Data for the selected and previous year
    selected_year_data = df_concussions[df_concussions['Season_Start'] == year].groupby('Team')['ID'].count().reset_index(name='Injuries')
    previous_year_data = df_concussions[df_concussions['Season_Start'] == year - 1].groupby('Team')['ID'].count().reset_index(name='Previous_Injuries')

    merged_data = pd.merge(selected_year_data, previous_year_data, on='Team', how='left')
    merged_data['Previous_Injuries'] = merged_data['Previous_Injuries'].fillna(0)
    merged_data['Injury_Difference'] = merged_data['Injuries'] - merged_data['Previous_Injuries']

    return merged_data.sort_values('Injury_Difference', ascending=False)

def create_injury_timeline(df_concussions, width=800, height=400):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Group by date and count injuries
    injury_timeline = df_concussions.groupby('Date')['ID'].count().reset_index(name='Injury_Count')

    # Create the line chart
    chart = alt.Chart(injury_timeline).mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(title="Date", titleFontSize=16, titlePadding=10)),
        y=alt.Y('Injury_Count:Q', axis=alt.Axis(title="Injury Count", titleFontSize=16, titlePadding=10)),
        tooltip=['Date:T', 'Injury_Count:Q']
    ).properties(
        width=width,
        height=height,
        title='Injury Timeline'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    return chart

def create_position_injury_chart(df_concussions, width=600, height=400, title_font_size=16, axis_font_size=14):
    if not isinstance(df_concussions, pd.DataFrame) or df_concussions.empty:
        raise ValueError("df_concussions must be a non-empty pandas DataFrame")

    # Group by position and count injuries
    position_injuries = df_concussions['Position'].value_counts().reset_index()
    position_injuries.columns = ['Position', 'Injury_Count']

    # Create the bar chart
    chart = alt.Chart(position_injuries).mark_bar().encode(
        x=alt.X('Position:N', axis=alt.Axis(title="Position", titleFontSize=axis_font_size, labelFontSize=12)),
        y=alt.Y('Injury_Count:Q', axis=alt.Axis(title="Injury Count", titleFontSize=axis_font_size, labelFontSize=12)),
        color=alt.Color('Position:N', legend=None),
        tooltip=['Position', 'Injury_Count']
    ).properties(
        width=width,
        height=height,
        title=alt.TitleParams(text='Injuries by Player Position', fontSize=title_font_size)
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=axis_font_size
    )

    return chart