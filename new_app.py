# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:01:56 2020

@author: juanp
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import os
import pathlib
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True
)
app.title = 'Favicon'
server = app.server


APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("rutas_ejemplo", "ejemplo_info.csv")))
df['fecha'] = pd.to_datetime(df['fecha'],format = '%Y-%m-%d')
df['fecha'] = df['fecha'].dt.strftime('%Y-%m-%d')
Rutas = df['ruta'].astype('category').cat.categories.tolist() 


colores = [ "#548B54",
            "#32CD32",
            "#228B22",
            "#00FF00",
            "#00EE00",
            "#00CD00",
            "#008B00",
            "#008000",
            "#006400",
            "#308014",
            "#7CFC00",
            "#7FFF00",
            "#76EE00",
            "#66CD00",
            "#458B00",
            "#ADFF2F",
            "#CAFF70",
            "#BCEE68",
            "#A2CD5A",
            "#6E8B3D",
            "#556B2F",
            "#6B8E23",
            "#C0FF3E",
            "#B3EE3A"]


hour_label ={}

for label,value in zip(['0'+str(hour)+':00' for hour in range(10)]+[str(hour)+':00' for hour in range(10,24)],range(24)):
    hour_label[value]=label



# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiYW5kZ3VleiIsImEiOiJja2Z6ZnY2bmMwem9kMnVvN2t1ZXh4Y3NoIn0.drQC38MoDwPrQAh_qUrI3g"

list_of_locations = {
    "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
    "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
    "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
    "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
    "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
    "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
    "Times Square": {"lat": 40.7589, "lon": -73.9851},
    "Columbia University": {"lat": 40.8075, "lon": -73.9626},
    "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
}


def build_banner():
    
    return html.Div(
        id = 'banner',
        className = 'banner',
        children = [
            html.Div(
                id = 'Banner - Text',
                children =[
                    html.H2("Carga de Pasajeros"),
                    html.H6("Área metropolitana del Valle de Aburrá")
                    ]
                ),
            html.Div(
                id = 'banner-logo',
                children = [
                    html.Button(
                        id = 'Description-button',
                        children = 'Descripcion',
                        n_clicks = 0
                        ),
                    html.A([
                        html.Img(
                            id = 'Logo',
                            src = 'https://sim.metropol.gov.co/welcome.png'
                            )
                        ], href = 'https://www.metropol.gov.co/'                        
                        )
                    ]
                )
            ]
        )

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Descripcion",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Prediccion",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this mock app about?

                        This is a dashboard for monitoring real-time process quality along manufacture production line.

                        ###### What does this app shows

                        Click on buttons in `Parameter` column to visualize details of measurement trendlines on the bottom panel.

                        The sparkline on top panel and control chart on bottom panel show Shewhart process monitor using mock data.
                        The trend is updated every other second to simulate real-time measurements. Data falling outside of six-sigma control limit are signals indicating 'Out of Control(OOC)', and will
                        trigger alerts instantly for a detailed checkup.
                        
                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab.

                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


@app.callback(
    Output("markdown", "style"),
    [Input("Description-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "Description-button":
            return {"display": "block"}

    return {"display": "none"}





def build_tab_1():
    return(
    html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Div(
                            className="div-for-dropdown",
                            children=[html.P('Ingrese la fecha que desea revisar'),
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=dt(2019, 1, 1),
                                    max_date_allowed=dt(2022, 1, 1),
                                    initial_visible_month=dt(dt.now().year, dt.now().month, dt.now().day),
                                    date=dt(dt.now().year, dt.now().month, dt.now().day).date(),
                                    display_format="MMMM D, YYYY",
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Ingrese la Ruta que desea revisar'),
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            options=[
                                                {"label": ruta, "value": ruta}
                                                for ruta in Rutas
                                            ],
                                            placeholder="Ruta",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Ingrese la hora que desea revisar'),
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="bar-selector",
                                            options=[
                                                {
                                                    "label": hour_label[value],
                                                    "value": value,
                                                }
                                                for value in hour_label.keys()
                                            ],
                                            multi=True,
                                            placeholder="Hora del dia",
                                        )
                                    ],
                                ),
                                html.Img(
                                    id = 'team-logo',
                                    src = 'assets/team_img.jpeg',
                                    style={'width':'100%'}
                                    
                                    )
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph"),
                        html.Div(
                            className="text-padding",
                            children=[
                                html.P("Select any of the bars on the histogram to section data by time.")
                            ],
                        ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        ),
    )


def build_tab_2():
    return (
        html.Div(
                id = 'tab2-content',
                children = [html.H2('En Desarrollo...')]
            ),
        )


@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    else:
        return build_tab_2()


# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [Input("date-picker", "date"), Input("location-dropdown", "value")],
    )
def update_histogram(date_picked, route_selected):
    if date_picked in df['fecha'].tolist():
        data = df[df['fecha'] == date_picked]
    else:
        data = df

    if route_selected:
        data = data[data['ruta'] == route_selected]

    xVal = []
    yVal = []

    for hour in hour_label:
        if hour in data['hora']:
            xVal.append(hour)
            yVal.append(int(data['carga'][data['hora'] == hour].sum()))

    xVal = pd.Series(xVal)
    yVal = pd.Series(yVal)

    colorVal = colores[:int(len(xVal))]

    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        dragmode="select",
        font=dict(color="black"),
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00",
        ),
        yaxis=dict(
        #   range=[0, max(yVal) + max(yVal) / 4],
            showticklabels=False,
            showgrid=False,
            fixedrange=True,
            rangemode="nonnegative",
            zeroline=False,
        ),
        annotations=[
            dict(
                x=xi,
                y=yi,
                text=str(yi),
                xanchor="center",
                yanchor="bottom",
                showarrow=False,
                font=dict(color="black"),
            )
            for xi, yi in zip(xVal, yVal)
        ],
    )

    return go.Figure(
        data=[
            go.Bar(x=xVal, y=yVal, marker=dict(color=colorVal), hoverinfo="x"),
            go.Scatter(
                opacity=0,
                x=xVal,
                y=yVal / 2,
                hoverinfo="none",
                mode="markers",
                marker=dict(color="rgb(66, 134, 244, 0)", symbol="square", size=40),
                visible=True,
            ),
        ],
        layout=layout,
    )


@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "date"),
        Input("location-dropdown", "value"),
    ],
)
def update_graph(date_picked, route_selected):
    zoom = 10.0
    latInitial = 6.2259489
    lonInitial = -75.6119972
    bearing = 0

    data = df

    if date_picked in df['fecha'].tolist():
        data = df[df['fecha'] == date_picked]

    if route_selected:
        data = data[data['ruta'] == route_selected]

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            Scattermapbox(
                lat=data["latitud"],
                lon=data["longitud"],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=data['hora'],
                marker=dict(
                    showscale=True,
                    color=np.append(np.insert(data['hora'].value_counts().index, 0, 0), 23),
                    opacity=0.5,
                    size=5,
                    colorscale=[
                        [0, "#F4EC15"],
                        [0.04167, "#DAF017"],
                        [0.0833, "#BBEC19"],
                        [0.125, "#9DE81B"],
                        [0.1667, "#80E41D"],
                        [0.2083, "#66E01F"],
                        [0.25, "#4CDC20"],
                        [0.292, "#34D822"],
                        [0.333, "#24D249"],
                        [0.375, "#25D042"],
                        [0.4167, "#26CC58"],
                        [0.4583, "#28C86D"],
                        [0.50, "#29C481"],
                        [0.54167, "#2AC093"],
                        [0.5833, "#2BBCA4"],
                        [1.0, "#613099"],
                    ],
                    colorbar=dict(
                        title="Time of<br>Day",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#d8d8d8"),
                        titlefont=dict(color="#d8d8d8"),
                        thicknessmode="pixels",
                    ),
                ),
            ),
            # Plot of important locations on the map
            Scattermapbox(
                lat=[i for i in data["latitud"]],
                lon=[i for i in data["longitud"]],
                mode="markers",
                hoverinfo="text",
                text=[i for i in data['carga']],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="streets",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-73.991251",
                                        "mapbox.center.lat": "40.7272",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "streets",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=3,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )


# Layout of Dash App
app.layout = html.Div(
    children=[build_banner(),
              html.Div(
                  id = 'app-container',
                  children = [
                      build_tabs(),
                      html.Div(
                          id = 'app-content'
                          )
                      ]
                  ),
              generate_modal()
            ]
        )








if __name__ == "__main__":
    app.run_server(debug=True)
