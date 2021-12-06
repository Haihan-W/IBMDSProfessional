#dash_interactivity.py

##########
#TASK 1 - Read the data
##########

# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})


##########
#TASK 2 - Create dash application and get the layout skeleton
#TASK 3 - Update layout components, e.g. Add the application title under html.H1() tag
										#Add the application description under html.P() tag
										#Update the graph under dcc.Graph() tag, 
										#Add Input Component using dcc.Input()
										#Add Output Component using dcc.Graph()...
##########

# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 (header 1) component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('Airline Performance Dashboard', #H1 component is Header 1
										style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),                                
								html.Div(["Input Year: ", #The first component of this div - a plain text
										  #The second component of this div - a dcc.input (user input box)
										  dcc.Input(id="input-year",type='number', # This is the Input component with user input box
																  value='2010',#default value = 2010 
																  style = {'height':'50px','font-size':35})], #style for the input box
    									style={'font-size':40}), #style for the whole sub-division html.Div(), in this case "Input Year: "'s text font
                                html.Br(), #Line Break element
                                html.Br(), #Line Break element
                                html.Div(dcc.Graph(id='line-plot')), #output component
                                ])


##########
#TASK 4 - Add the application callback function
##########

#The core idea of this application is to get year as user input and update the dashboard in **real-time**. We will be using callback function for the same.

# add callback decorator
@app.callback(Output(component_id='line-plot', component_property='figure'), #Output is connected to Dash's dcc.Graph's id, note the same id name
               Input(component_id='input-year', component_property='value')) #Input is connected to Dash's dcc.Input's id, note the same id name

# Add computation to callback function and return graph - any function defined under callback decorator above will be automatically executed whenever user changes the input
def get_graph(entered_year): #Input of this function is connected to "Input" in callback decorator, Output of this function is connected to "Output" in callback decorator
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute average over arrival delay time.
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    
    # plot figure
    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))

    # define layout: e.g. figure title, xaxis title, yaxis title
    fig.update_layout(title='ArrDelay vs Month', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()