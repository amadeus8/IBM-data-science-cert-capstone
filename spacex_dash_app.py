# Import required libraries
import pandas as pd
import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                                id='site-dropdown',
                                                options=[   {'label': 'All Sites', 'value': 'ALL'},
                                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                            {'label': 'VAFB SCL-4E', 'value': 'VAFB SCL-4E'},
                                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}],
                                                value='ALL',
                                                placeholder='Select site...',
                                                searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000,
                                                step=1000,
                                                marks={0:'0', 100:'100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(  Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Successful Launches by Site')
        return fig
    
    else:
        filtered_series = spacex_df[spacex_df['Launch Site'] == entered_site]['class']

        counts = filtered_series.value_counts().rename(index={0: 'Failure', 1: 'Success'})
        counts_df = counts.reset_index()
        counts_df.columns = ['Outcome', 'Count']

        fig = px.pie(
            counts_df,
            values='Count',
            names='Outcome',
            title=f'Total Successful Launches for Site {entered_site}'
        )
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(  Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload):
#     A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
    filtered_df = spacex_df
    # If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg)
    # and variable class.
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Launches by Site and Payload Mass(kg)')
        return fig
    
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
        min_payload, max_payload = payload
        filtered_df = filtered_df[
            (filtered_df['Payload Mass (kg)'] >= min_payload) &
            (filtered_df['Payload Mass (kg)'] <= max_payload)
        ]
        
        fig = px.scatter(filtered_df,
                        x='Payload Mass (kg)',
                        y='class',
                        title=f'Launches by Site {entered_site} and Payload Mass {payload} (kg)')
            
        return fig
# In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
# If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show
# values Payload Mass (kg) and class for the selected site, and color-label the point using Boosster Version Category likewise.


# Run the app
if __name__ == '__main__':
    app.run()
