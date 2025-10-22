import plotly.io as pio
import plotly.express as px
import pandas as pd
import json

from urllib.request import urlopen
import json

### import graph to front end ###

def create_forest_graph():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    forest_df = pd.read_csv('csv/forest.csv')
    df = {'locations': forest_df['country_code'].tolist(), 'Deforestation': forest_df['deforestation'].tolist()}
    custom_colorscale = [
        [0, "rgb(3, 74, 1)"],
        [.04, "rgb(3, 74, 1)"],
        [.15, "rgb(255, 235, 15)"],
        [.30,"rgb(255, 147, 15)"],
        [.40,"rgb(163, 3, 19)"],
        [.6,"rgb(158, 2,   51)"],
        [.9,"rgb(89,  0,   18)"],
        [1,"rgb(89,  0,   18)"]
    ]
    fig = px.choropleth(
        df, geojson=counties, locations='locations', color='Deforestation',
        locationmode="ISO-3", color_continuous_scale=custom_colorscale,
        range_color=(0, 500), labels={'Deforestation':'Deforestation Rate (%)'}
    )
    fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0}, title="World Map of Deforestation Rate")
    
    return fig.to_json()