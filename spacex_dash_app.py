# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()  # for the slider option
min_payload = spacex_df['Payload Mass (kg)'].min()  # for the slider option

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                # Add a divison
                                html.Div([
                                    # Create a division that holds the header of the selections
                                    html.Div([
                                        html.H2('Launch Site:', style={'margin-right': '2em'})
                                    ]),
                                    dcc.Dropdown(id='site-dropdown',
                                                 options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'Cape Canaveral Space Launch Complex 40 - CCAFS LC-40', 'value': 'OPT1'},
                                                    {'label': 'Cape Canaveral Space Launch Complex 40 - CCAFS SLC-40', 'value': 'OPT2'},
                                                    {'label': 'Kennedy Space Center Launch Complex 39 - KSC LC-39A', 'value': 'OPT3'},
                                                    {'label': 'Vandenberg Space Launch Complex 4 - VAFB SLC-4E', 'value': 'OPT4'}
                                                 ],
                                                 value="ALL",
                                                 placeholder="Select Launch Site",
                                                 searchable=True),
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected,show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', style={'display': 'flex'})),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       1000: '1000',
                                                       2000: '2000',
                                                       3000: '3000',
                                                       4000: '4000',
                                                       5000: '5000',
                                                       6000: '6000',
                                                       7000: '7000',
                                                       8000: '8000',
                                                       9000: '9000',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
    else:
        # return the outcomes piechart for a selected site
        if entered_site == 'OPT1':
            site = filtered_df[filtered_df["Launch Site"] == 'CCAFS LC-40']
            fig = px.pie(site, values='Flight Number',
            names = 'class',
            title = 'Total Success Launches for site CCAFS LC-40')
        elif entered_site == 'OPT2':
            site = filtered_df[filtered_df["Launch Site"] == 'CCAFS SLC-40']
            fig = px.pie(site, values='Flight Number',
            names = 'class',
            title = 'Total Success Launches for site CCAFS SLC-40')
        elif entered_site == 'OPT3':
            site = filtered_df[filtered_df["Launch Site"] == 'KSC LC-39A']
            fig = px.pie(site, values='Flight Number',
            names = 'class',
            title = 'STotal Success Launches for site KSC LC-39A')
        else:
            site = filtered_df[filtered_df["Launch Site"] == 'VAFB SLC-4E']
            fig = px.pie(site, values='Flight Number',
            names = 'class',
            title = 'Total Success Launches for site VAFB SLC-4E')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(entered_site, entered_payload):
    filtered_df = spacex_df
    payload_range = filtered_df[(filtered_df["Payload Mass (kg)"] >= entered_payload[0]) & (filtered_df["Payload Mass (kg)"] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(payload_range,
                         x="Payload Mass (kg)",
                         y="class",
                         color="Booster Version Category",
                         title="Correlation between Payload and Success for all Sites")
    else:
        if entered_site == 'OPT1':
            site = payload_range[payload_range["Launch Site"] == 'CCAFS LC-40']
            fig = px.scatter(site,
                             x="Payload Mass (kg)",
                             y="class",
                             color="Booster Version Category",
                             title="Correlation between Payload and Success for site CCAFS LC-40")
        elif entered_site == 'OPT2':
            site = payload_range[payload_range["Launch Site"] == 'CCAFS SLC-40']
            fig = px.scatter(site,
                             x="Payload Mass (kg)",
                             y="class",
                             color="Booster Version Category",
                             title="Correlation between Payload and Success for site CCAFS SLC-40")
        elif entered_site == 'OPT3':
            site = payload_range[payload_range["Launch Site"] == 'KSC LC-39A']
            fig = px.scatter(site,
                             x="Payload Mass (kg)",
                             y="class",
                             color="Booster Version Category",
                             title="Correlation between Payload and Success for site KSC LC-39A")
        else:
            site = payload_range[payload_range["Launch Site"] == 'VAFB SLC-4E']
            fig = px.scatter(site,
                             x="Payload Mass (kg)",
                             y="class",
                             color="Booster Version Category",
                             title="Correlation between Payload and Success for site VAFB SLC-4E")
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
