# Import required libraries

import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("E:\Documents\ITDUKE\Data science\IBM_DS_Prof_Cert\Courses data\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# creating option list with extra 'ALL Sites' value
options_list = []
options_list = ["All sites"]
options_list.extend(list(spacex_df["Launch Site"].unique()))

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

                                # create a Division and add dropdown
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="site-dropdown",
                                            options=[{"label": i, "value": i} for i in options_list],
                                            value="All sites",
                                            placeholder="All sites",
                                            searchable=True,
                                        )
                                    ]
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(
                                    dcc.Graph(
                                        id='success-pie-chart'
                                    )
                                ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    marks={0: {"label" : "0"},
                                           2500: {"label" : "2500"},
                                           5000: {"label" : "5000"},
                                           7500: {"label" : "7500"}},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(
                                        id='success-payload-scatter-chart'

                                    )
                                ),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def getPieChart(selected_site):
    if selected_site == "All sites":
        pie_fig = px.pie(spacex_df, values="class", names="Launch Site",
                         title="Total Success Launches by Site")

    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        filtered_df = filtered_df.groupby(["Launch Site", "class"]).size().reset_index(name="counts")
        pie_fig = px.pie(filtered_df, values="counts", names="class",
                         title="Total Success Launches for Site {}".format(selected_site))

    return pie_fig

@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="site-dropdown", component_property="value"),
     Input(component_id="payload-slider", component_property="value")]
    )

def ScatterPlot(selected_site, payload):

    # filter dataframe for payload selected [0] is for low and [1] is for high value selected by RangeSlider
    filtered_df = spacex_df[(payload[0] <= spacex_df["Payload Mass (kg)"])  &
                            (spacex_df["Payload Mass (kg)"] <= payload[1])]

    # if all sites
    if selected_site == "All sites":
        scat_fig = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class", color= "Booster Version Category",
                              symbol= "Launch Site")
    else:
        filtered_df = filtered_df[filtered_df["Launch Site"] == selected_site]
        scat_fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")

    return scat_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug= True, dev_tools_ui=True, dev_tools_props_check=True)


# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:
#
# Which site has the largest successful launches?
## KSC LC-39A

# Which site has the highest launch success rate?
## KSC LC-39A

# Which payload range(s) has the highest launch success rate?
## 1900-5300

# Which payload range(s) has the lowest launch success rate?
## 500-1900 & 5350-6800

# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
## KSC LC-39A