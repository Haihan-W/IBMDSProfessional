# dash_layout.py

# Import required packages
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

## Add Dataframe
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "NYC", "MTL", "NYC"]
})

## Add a bar graph figure
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

## Create Dash Layout
app = dash.Dash()
app.layout = html.Div(children=[
    #1. Create Header
    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center'
        }
    ),
    
    #2. Create dropdown
    dcc.Dropdown(options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='NYC' # Providing a default value to dropdown
    ),

    #3. Bar graph
    dcc.Graph(id='example-graph-1',figure=fig)
])

## Run Application
if __name__ == '__main__':
    app.run_server()