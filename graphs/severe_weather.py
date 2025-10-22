import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd  # Added missing pandas import

# Load ocean level data from CSV
# df = pd.read_csv('csv/severe_weather.csv')

# trace1 = go.Scatter(x=df[df['location'] == 'North America']['year'],
#                     y=df[df['location'] == 'North America']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=3,
#                     name='North America',
#                     marker=dict(size=15))

# trace2 = go.Scatter(x=df[df['location'] == 'South America']['year'],
#                     y=df[df['location'] == 'South America']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=1, 
#                     name='South America',
#                     marker=dict(size=15))

# trace3 = go.Scatter(x=df[df['location'] == 'Africa']['year'],
#                     y=df[df['location'] == 'Africa']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=2,
#                     name='Africa',
#                     marker=dict(size=15))

# trace4 = go.Scatter(x=df[df['location'] == 'Asia']['year'],
#                     y=df[df['location'] == 'Asia']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=4,
#                     name='Asia',
#                     marker=dict(size=15))

# trace5 = go.Scatter(x=df[df['location'] == 'Europe']['year'],
#                     y=df[df['location'] == 'Europe']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=5,
#                     name='Europe',
#                     marker=dict(size=15))

# trace6 = go.Scatter(x=df[df['location'] == 'Australia']['year'],
#                     y=df[df['location'] == 'Australia']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=5,
#                     name='Australia',
#                     marker=dict(size=15))

# trace7 = go.Scatter(x=df[df['location'] == 'Antarctica']['year'],
#                     y=df[df['location'] == 'Antarctica']['# of Severe Weather Events'],
#                     mode='lines+markers',
#                     zorder=5,
#                     name='Antarctica',
#                     marker=dict(size=15))

# layout = go.Layout(
#     title=dict(text='Ocean Levels Over Time'),
#     xaxis=dict(title='Year'),
#     yaxis=dict(title='Sea Level Change (mm)')
# )

# fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5], layout=layout)

# fig.show()

# with open('graphs/severe_weather_graph.json', 'w') as f:
#     f.write(fig.to_json())


# ### make graph for front end ###
def create_severe_weather_graph():
    df = pd.read_csv('csv/severe_weather.csv')
    traces = []
    regions = df['location'].unique()
    for region in regions:
        traces.append(go.Scatter(
            x=df[df['location'] == region]['year'],
            y=df[df['location'] == region]['# of Severe Weather Events'],
            mode='lines+markers',
            name=region,
            marker=dict(size=15)
        ))
    layout = go.Layout(
        title=dict(text='Severe Weather Events By Region'),
        xaxis=dict(title='Year'),
        yaxis=dict(title='# of Severe Weather Events')
    )
    fig = go.Figure(data=traces, layout=layout)
    
    return fig.to_json()