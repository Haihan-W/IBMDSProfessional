# flight_details.py


##########
#TASK 1 - Read the data
##########

# Import required libraries
import pandas as pd
# import plotly.graph_objects as go
import plotly.express as px
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

# Build dash app layout
app.layout = html.Div(children=[#Header component
								html.H1('Flight Delay Time Statistics',
										style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}), 
								
								#Input component
                                html.Div(["Input Year: ", 
                                		dcc.Input(id='input-year', value = '2010', type = 'number',
                                				style = {'height':'35px','font-size':30})], # input box's style
                                style={'font-size': 30}), #"Input Year: "'s text font


                                html.Br(), #Line Break element
                                html.Br(), #Line Break element


                                #Output Component: 3 segments, first 2 segments are divided to two sub-sections; in total 2+2+1 = 5 graph outputs
                                
                                ## segment 1:
                                html.Div([
                                		#sub-section 1:
                                        html.Div(dcc.Graph(id='carrier-plot')),

                                        #sub-section 2:
                                        html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
    							

    							## segment 2:
                                html.Div([
                                		#sub-section 1:
                                        html.Div(dcc.Graph(id='nas-plot')),

                                        #sub-section 2:
                                        html.Div(dcc.Graph(id='security-plot'))
                                ], style={'display': 'flex'}),
                                

                                ## segment 3:
                                html.Div(dcc.Graph(id='late-plot'), 
                                		 style={'width':'65%'})
                                ])



##########
#TASK 4 - Add supporting function
##########

""" Compute_info function description

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    airline_data: Input airline data.
    entered_year: Input year for which computation needs to be performed.
    
Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.

"""
def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


##########
#TASK 5 - Add the application callback function
##########

# Callback decorator, note: multiple output can be combined as a list [output1,output2,...]
@app.callback( [
               Output(component_id='carrier-plot', component_property='figure'), # 1. THE ORDER!! of this callback decorator's output should match callback function's return order; 
               Output(component_id='weather-plot', component_property='figure'), # 2. id of this callback decorator's output should match layout html div's dcc.graph's id. 
               Output(component_id='nas-plot', component_property='figure'),     # 3. property = 'figure' because id was defined under dcc.graph() in layout section above;
               Output(component_id='security-plot', component_property='figure'), # 4. If id was defined directly under html.Div(), then property = 'children' (see Week 5 -> Lab1_2_Dash_Auto.py)
               Output(component_id='late-plot', component_property='figure'),
               ],
               Input(component_id='input-year', component_property='value'))
# Computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
            
    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrier delay time (minutes) by airline')
    # Line plot for weather delay
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
    # Line plot for NAS (national air system) delay
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS (national air system) delay time (minutes) by airline')
    # Line plot for security delay
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')
    # Line plot for late aircraft delay
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average Late Aircraft delay time (minutes) by airline')
            
    return[carrier_fig, weather_fig, nas_fig, sec_fig, late_fig] #THE ORDER!! of this callback function return should match @callback decorator's OUTPUT order

# Run the app
if __name__ == '__main__':
    app.run_server()

