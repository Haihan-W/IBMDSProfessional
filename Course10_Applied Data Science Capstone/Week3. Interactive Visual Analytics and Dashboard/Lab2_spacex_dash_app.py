# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print('max ',max_payload,'min ',min_payload)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},],
                                    value = 'All',
                                    placeholder = "Select a Launch Site Here",
                                    searchable = True),
                                html.Br(), #line break element

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max = 10000, step = 1000,
                                    marks = {0: '0 kg',
                                            2500: '2500',
                                            5000: '5000',
                                            7500: '7500',
                                            10000: '10000'
                                            }, #tickle on range slider
                                    value=[min_payload,max_payload]),
                                    # value defined default min and max selected range when initial loading the dash
                                    # min_payload, max_payload was defined before

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches Count by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).count().reset_index().rename(columns={'Unnamed: 0':'counts'})
        #source: https://stackoverflow.com/a/32801170
        #count() is used to return row count for each group, the result is a series object with one column for count, and indexes for series are 'Launch Site' and 'class'
        #name='counts' is used to give the series above a column name.
        #reset_index() is used to convert series above to a dataframe, with reseted index (index start from 0,1,...)
            #instead of using 'Launch Site' and 'class' as index        
        fig = px.pie(filtered_df, values='counts', 
        names='class', 
        title='Total Success Launches vs. Unsuccess Launches for site ' + entered_site)
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), 
                Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)']<payload_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x ='Payload Mass (kg)', y = 'class',
        color='Booster Version Category', 
        title='Success vs. Payload for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)']<payload_range[1]) &
                            (spacex_df["Launch Site"]==entered_site)]     
        fig = px.scatter(filtered_df, x ='Payload Mass (kg)', y = 'class',
        color='Booster Version Category', 
        title='Success vs. Payload for Site ' + entered_site)
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
