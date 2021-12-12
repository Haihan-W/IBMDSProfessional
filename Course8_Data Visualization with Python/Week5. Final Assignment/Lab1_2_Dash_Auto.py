#Dash_Auto.py

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the automobiles data into pandas dataframe
auto_data =  pd.read_csv('automobileEDA.csv', 
                            encoding = "ISO-8859-1",
                            )

#Layout Section of Dash

app.layout = html.Div(children=[
	#Create Header
	html.H1('Car Automobile Components', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 24}),


    #outer division starts
    html.Div(children=[

       # First inner divsion for adding dropdown + its helper text for Selected Drive wheels
        html.Div(children=[
	                #Create Header for the first Inner Division
	                html.H2('Drive Wheels Type:', style={'margin-right': '2em'}),
	                #Create Dropdown
					dcc.Dropdown(
					    id='demo-dropdown',
				        options=[
				            {'label': 'Rear Wheel Drive', 'value': 'rwd'},
				            {'label': 'Front Wheel Drive', 'value': 'fwd'},
				            {'label': 'Four Wheel Drive', 'value': '4wd'}
						],
						value='rwd'
					),
		]),
		# End of First Inner Div #
        

        #Second Inner division for adding 2 inner divisions for 2 output graphs 
        html.Div(children=[
        	
        	html.Div([ ], id='plot1'),
        	html.Div([ ], id='plot2')
            
        ], style={'display': 'flex'}), #'display'="Flex" will place elements inside 'children' next to each other (i.e. in the same row)
        # End of Second Inner Div #


	])
    # End of outer division #

])
# End of layout #

#add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='children'), #1. Here, the component property = 'children' instead of 'figure', because: id was defined directly under html.Div() in layout section above, 
																			 # rather than inside dcc.Graph() as in Week 4 -> Lab4_1_flight_details.py; 
																			 # Here we have created empty division [] in layout section above with id (e.g. 'plot1') and passing entire dcc.Graph (figure) as return of callback function, instead of figure object as in Week 4 -> Lab4_1_flight_details.py.
               Output(component_id='plot2', component_property='children')], # 2. THE ORDER!! of this callback decorator's output should match callback function's return order; 
               Input(component_id='demo-dropdown', component_property='value'))
   
#define the callback function
def display_selected_drive_charts(input_value):
   

   
   filtered_df = auto_data[auto_data['drive-wheels']==input_value].groupby(['drive-wheels','body-style'],as_index=False). \
            	mean() # It will calculate "mean" of every numerical column ("price" col is one of them) based on each group defined at groupby parameters above, 
            			#the non-numerical cols which is not in groupby parameters col name, will be automatically excluded from resulting dataframe "filtered_df" 
        				#In the pie chart/bar chart below, if you only want to use mean "price" for each group, just specify "price" column from resulting df, in pie/bar chart parameters. 
   filtered_df = filtered_df
   
   fig1 = px.pie(filtered_df, values='price', names='body-style', title="Pie Chart")
   fig2 = px.bar(filtered_df, x='body-style', y='price', title='Bar Chart')
    
   return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2) ] #THE ORDER!! of this callback function return should match @callback decorator's OUTPUT order
   
   


if __name__ == '__main__':
    app.run_server()