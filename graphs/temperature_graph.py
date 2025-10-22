import plotly.io as pio
import plotly.express as px
import pandas as pd
import json

from urllib.request import urlopen
import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     countries = json.load(response)

# df = pd.read_csv("csv/temperature.csv")

# custom_colorscale = [
#         [0, "rgb(3, 202, 252)"],
#         [.2, "rgb(3, 202, 252)"],
#         [.5, "rgb(255, 255, 255)"],
#         [.8, "rgb(247, 69, 81)"],
#         [1, "rgb(247, 69, 81)"]
#     ]

# fig = px.choropleth(df, geojson=countries, locations='locations', color='temp',
#                            locationmode="ISO-3",
#                            color_continuous_scale=custom_colorscale,
#                            range_color=(-20, 40),
#                            labels={'temp':'Temperature'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title="World Map of Average Temperatures (celsius)")
# graph_json = json.dumps(fig.to_json())

# with open('graphs/temperature_graph.json', 'w') as f:
#     f.write(fig.to_json())


# ### Make graphs for html ###
def create_temperature_graph():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        countries = json.load(response)
    df = pd.read_csv("csv/temperature.csv")
    custom_colorscale = [
        [0, "rgb(3, 202, 252)"],
        [.2, "rgb(3, 202, 252)"],
        [.5, "rgb(255, 255, 255)"],
        [.8, "rgb(247, 69, 81)"],
        [1, "rgb(247, 69, 81)"]
    ]
    fig = px.choropleth(
        df, geojson=countries, locations='locations', color='temp',
        locationmode="ISO-3", color_continuous_scale=custom_colorscale,
        range_color=(-20, 40), labels={'temp': 'Tmp (C)'}
    )
    fig.update_layout(margin={"r":0, "t":100, "l":0, "b":0}, title="World Map of Avg. Temperatures (Celsius)")
   
    return fig.to_json()