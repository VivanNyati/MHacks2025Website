import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd  # Added missing pandas import

# Load ocean level data from CSV
# df = pd.read_csv('csv/ocean_levels.csv')

# trace1 = go.Scatter(x=df[df['location'] == 'Pacific']['year'],
#                     y=df[df['location'] == 'Pacific']['Sea Level'],
#                     mode='lines+markers',
#                     zorder=3,
#                     name='Pacific',
#                     marker=dict(size=15))

# trace2 = go.Scatter(x=df[df['location'] == 'Atlantic']['year'],
#                     y=df[df['location'] == 'Atlantic']['Sea Level'],
#                     mode='lines+markers',
#                     zorder=1, 
#                     name='Atlantic',
#                     marker=dict(size=15))

# trace3 = go.Scatter(x=df[df['location'] == 'Indian Ocean']['year'],
#                     y=df[df['location'] == 'Indian Ocean']['Sea Level'],
#                     mode='lines+markers',
#                     zorder=2,
#                     name='Indian',
#                     marker=dict(size=15))

# trace4 = go.Scatter(x=df[df['location'] == 'Southern']['year'],
#                     y=df[df['location'] == 'Southern']['Sea Level'],
#                     mode='lines+markers',
#                     zorder=4,
#                     name='Southern',
#                     marker=dict(size=15))

# trace5 = go.Scatter(x=df[df['location'] == 'Arctic']['year'],
#                     y=df[df['location'] == 'Arctic']['Sea Level'],
#                     mode='lines+markers',
#                     zorder=5,
#                     name='Arctic',
#                     marker=dict(size=15))

# layout = go.Layout(
#     title=dict(text='Ocean Levels Over Time'),
#     xaxis=dict(title='Year'),
#     yaxis=dict(title='Sea Level Change (mm)')
# )

# fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5], layout=layout)

# fig.show()

# with open('graphs/ocean_levels_graph.json', 'w') as f:
#     f.write(fig.to_json())

# ### import graph to front end ###
def create_ocean_levels_graph():
    df = pd.read_csv('csv/ocean_levels.csv')
    traces = []
    regions = df['location'].unique()
    for region in regions:
        traces.append(go.Scatter(
            x=df[df['location'] == region]['year'],
            y=df[df['location'] == region]['Sea Level'],
            mode='lines+markers',
            name=region,
            marker=dict(size=15)
        ))
    layout = go.Layout(
        title=dict(text='Ocean Levels Over Time'),
        xaxis=dict(title='Year'),
        yaxis=dict(title='Sea Level Change (mm)')
    )
    fig = go.Figure(data=traces, layout=layout)
    
    return fig.to_json()