# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:01:56 2020
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import numpy as np
from utils.query_utils import Sql, Carga_query, Arco_query


#
# # OBJECTS INITIALIZATION
#

app = dash.Dash(
    _name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width"}],
    suppress_callback_exceptions=True
)
app.title = 'AmvApp'
server = app.server

# Start query objects
sql = Sql()
cargaQuery = Carga_query()
arcoQuery = Arco_query()

# Could be deleted

hour_label ={}
for label,value in zip(['0'+str(hour)+':00' for hour in range(10)]+[str(hour)+':00' for hour in range(10,24)],range(24)):
    hour_label[value] = label

#
# # CONSTATNTS
#

mapbox_access_token = "pk.eyJ1IjoiYW5kZ3VleiIsImEiOiJja2Z6ZnY2bmMwem9kMnVvN2t1ZXh4Y3NoIn0.drQC38MoDwPrQAh_qUrI3g"

df_arcos = sql.request(query=arcoQuery.get_arco_query())

#
# # Functions
#


def generate_modal():
    """
    LinuxThingy version 1.6.5

    Parameters:

    -t (--text): show the text interface
    -h (--help): display this help
    """
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
                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab."""
                            )
                        ),
                    ),
                ],
            )
        ),
    )


def map_links(df):

    """
    This function return a plot of the map
    """

    streetsPLot = Scattermapbox(
                text=df['text'],
                lat=df['latitud'],
                lon=df['longitud'],
                hoverinfo='text',
                mode="markers",
                marker=dict(
                    allowoverlap=True,
                    showscale=True,
                    color=df['carga'],
                    opacity=1,
                    size=5,
                    colorscale=[
                        [0, "#36FF00"],
                        [0.25, "#FFF300"],
                        [1.0, "#FF0000"],
                    ],
                    colorbar=dict(
                        title="Carga",
                        x=0.93,
                        xpad=0,
                        nticks=24,
                        tickfont=dict(color="#000000"),
                        titlefont=dict(color="#000000"),
                        thicknessmode="pixels",
                    ),
                )
            )
    return streetsPLot

#
# # GUI
#


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
                        children = 'Información',
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
                        id="Project-tab",
                        label="Projecto",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Specs-tab",
                        label="Descripción",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Predicción",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-heatmap",
                        label="Subidas y bajadas",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def build_tab_1():
    return (
                html.Div(
                        children = [html.P('PRESENTACION AQUI')]
                        )
    )


def build_tab_2():
    return(
    html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                            html.Div(
                                children=[
                                    dcc.Graph(id="histogram")
                                ],
                            ),
                        #    html.Img(
                        #        id='team-logo',
                        #        src='assets/team_img.jpeg',
                        #        style={'width': '100%'}
                        #),
                        # Change to side-by-side for mobile layout
                        html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Seleccione un metodo de agrupacion'),
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="Agr-selector",
                                            options=[
                                                {
                                                    "label": 'Suma',
                                                    "value": 'SUM',
                                                },
                                                {
                                                    "label": 'Promedio',
                                                    "value": 'AVG',
                                                }
                                            ],
                                            multi=False,
                                            placeholder="Metodo de agrupacion",
                                            value='SUM'
                                        )
                                    ],
                                ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                        className="div-for-dropdown",
                                        children = [html.P('Ingrese la fecha que desea revisar'),
                                            dcc.DatePickerRange(
                                                id="date-picker",
                                                #min_date_allowed=df['fecha'].min(),
                                                #max_date_allowed=df['fecha'].max(),
                                                initial_visible_month=dt(dt.now().year, dt.now().month, dt.now().day),
                                                start_date='2019-11-11',
                                                end_date='2019-11-20',
                                                display_format="MMMM D, YYYY",
                                                #style={'backgroud': 'blue'},
                                            )
                                        ],
                                    ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Seleccione un dia de la semana'),
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="ruta-dropdown",
                                            options=[
                                                {"label": dia, "value": idx}
                                                for idx, dia in enumerate(['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'])
                                            ],
                                            multi=True,
                                            placeholder="Dia",
                                            searchable=True
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Ingrese la hora que desea revisar'),
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="hour-selector",
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
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-white",
                    children=[
                        dcc.Graph(id="map-graph"),
                        dcc.Markdown(
                            className='Map-text',
                            children=(
                                """
                        ###### DESCRIPCION DE MAP DE CARGAS AQUI
                        """
                            )
                        )
                    ],
                ),
            ],
        ),
    )


def build_tab_3():
    return(html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                            html.Div(
                            children=[
                                dcc.Graph(id="histogram-prediccion"),
                            ],
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children = [html.P('Ingrese la fecha que desea revisar'),
                                dcc.DatePickerRange(
                                    id="date-picker-prediccion",
                                    min_date_allowed=df['fecha'].min(),
                                    max_date_allowed=df['fecha'].max(),
                                    initial_visible_month=dt(dt.now().year, dt.now().month, dt.now().day),
                                    end_date=dt(dt.now().year, dt.now().month, dt.now().day).date(),
                                    display_format="MMMM D, YYYY",
                                    style={'backgroud': 'blue'},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Seleccione un dia de la semana'),
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="ruta-dropdown-prediccion",
                                            options=[
                                                {"label": dia, "value": idx}
                                                for idx, dia in enumerate(['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'])
                                            ],
                                            multi=True,
                                            placeholder="Dia",
                                            searchable=True
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Ingrese la hora que desea revisar'),
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="hour-selector-prediccion",
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
                                html.Button('Limpiar', id='limpiar-prediccion', n_clicks=0),
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-white",
                    children=[
                        dcc.Graph(id="map-graph",animate=True),
                        dcc.Markdown(
                            className='Map-text',
                            children=(
                                """
                        ###### What is this mock app about?

                        This is a dashboard for monitoring real-time process quality along manufacture production line.

                        ###### What does this app shows

                        Click on buttons in `Parameter` column to visualize details of measurement trendlines on the bottom panel.

                        The sparkline on top panel and control chart on bottom panel show Shewhart process monitor using mock data.
                        The trend is updated every other second to simulate real-time measurements. Data falling outside of six-sigma control limit are signals indicating 'Out of Control(OOC)', and will
                        trigger alerts instantly for a detailed checkup.
                        Operators may stop measurement by clicking on `Stop` button, and edit specification parameters by clicking specification tab."""
                            )
                        )
                    ],
                ),
            ],
        ),
    )


def build_tab_4():
    return(html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Div(
                            className="div-for-dropdown",
                            children = [html.P('Ingrese la fecha que desea revisar'),
                                dcc.DatePickerRange(
                                    id="date-picker-prediccion",
                                    min_date_allowed=df['fecha'].min(),
                                    max_date_allowed=df['fecha'].max(),
                                    initial_visible_month=dt(dt.now().year, dt.now().month, dt.now().day),
                                    end_date=dt(dt.now().year, dt.now().month, dt.now().day).date(),
                                    display_format="MMMM D, YYYY",
                                    style={'backgroud': 'blue'},
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Seleccione un dia de la semana'),
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="ruta-dropdown-prediccion",
                                            options=[
                                                {"label": dia, "value": idx}
                                                for idx, dia in enumerate(['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'])
                                            ],
                                            multi=True,
                                            placeholder="Dia",
                                            searchable=True
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[html.P('Ingrese la hora que desea revisar'),
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="hour-selector-prediccion",
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
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-white",
                    children=[
                        dcc.Graph(id="map-graph",animate=True),
                        dcc.Markdown(
                            className='Map-text',
                            children=(
                                """
                        ###### DESCRIPCION DE HEATMAP AQUI
                        """
                            )
                        )
                    ],
                ),
            ],
        ),
    )


#
# # CALLBACKS
#

# # Tabs

@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    elif tab_switch == "tab2":
        return build_tab_2()
    elif tab_switch == "tab3":
        return build_tab_3()
    else:
        return build_tab_4()

# # Descripcion

# Update Histogram Figure based on Month, Day and Times Chosen
@app.callback(
    Output("histogram", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("ruta-dropdown", "value"),
        Input("hour-selector", "value"),
        Input("Agr-selector", "value")
    ],
    )
def update_histogram(start_date, end_date, day_selected, hour_picked, agr_picked):
    """import data """
    print(agr_picked)
    cargaQuery.restart_query(update_map=False, agr=agr_picked)
    cargaQuery.add_date_range(start_date, end_date)
    cargaQuery.add_day_filter(day_selected)
    cargaQuery.add_hour_filter(hour_picked)
    cargaQuery.last_add()
    df_cargas = sql.request(cargaQuery.query)



    layout = go.Layout(
        bargap=0.01,
        bargroupgap=0,
        barmode="group",
        margin=go.layout.Margin(l=10, r=10, t=50, b=50),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        title="Carga total por hora",
        #dragmode="select",
        font=dict(color="black"),
        xaxis=dict(
            range=[-0.5, 23.5],
            showgrid=False,
            nticks=25,
            fixedrange=True,
            ticksuffix=":00",
        ),
        yaxis=dict(
            range=[0, df_cargas['carga'].max()],
            rangemode="nonnegative",
        ),
    )

    return go.Figure(
        data=[
            go.Bar(x=df_cargas['hora'], y=df_cargas['carga'], width=1, marker_color='#4682B4', hoverinfo="y"),  # marker=dict(color=colorVal),
        ],
        layout=layout,
    )


@app.callback(
    Output("map-graph", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("ruta-dropdown", "value"),
        Input("hour-selector", "value"),
        Input("Agr-selector", "value")
    ],
)
def update_map_descripcion(start_date, end_date, day_selected, hour_picked, agr_picked):
    zoom = 13
    latInitial = 6.2259489
    lonInitial = -75.6119972
    bearing = 0

    """import data """
    cargaQuery.restart_query(agr=agr_picked)
    cargaQuery.add_date_range(start_date, end_date)
    cargaQuery.add_day_filter(day_selected)
    cargaQuery.add_hour_filter(hour_picked)
    cargaQuery.last_add()
    df_cargas = sql.request(cargaQuery.query)

    """Assign loads to the streets"""
    df_full = df_arcos.merge(df_cargas, how='left', left_on='arco', right_on='arco', validate="m:1")
    df_full.dropna(inplace=True)

    if len(df_full['carga']) != 0:
        df_full['carga'] = df_full['carga'].astype(np.uint8)
        df_full['text'] = df_full.apply(lambda x:  '<b>Arco: </b> {} <br><b>Carga</b>: {}<br>'.format(x['arco'], x['carga']), axis=1)
    else:
        df_full['text'] = None
    return go.Figure(
        data=[
            map_links(df_full)  # Plot all streets
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),
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

# # Prediccion

@app.callback(
    Output("map-graph-prediccion", "figure"),
    [
        Input("date-picker-prediccion", "start_date"),
        Input("date-picker-prediccion", "end_date"),
        Input("ruta-dropdown-prediccion", "value"),
        Input("hour-selector-prediccion", "value")
    ],
)
def update_map_prediccion(start_date, end_date, day_selected, hour_picked):
    zoom = 10.0
    latInitial = 6.2259489
    lonInitial = -75.6119972
    bearing = 0

    data = df.copy()

    """import data"""
    df_arcos = pd.read_csv('Tablas/arcos.csv', index_col=0)
    df_cargas = pd.read_csv('Tablas/tabla_consulta.csv', index_col=0)

    """Assign loads to the streets"""
    df_cargas.drop_duplicates(subset=['Arco'], inplace=True)
    df_full = df_arcos.merge(df_cargas, how='left', on='Arco', validate="m:1")

    if start_date and end_date:
        try:
            data = data[(data['fecha'] >= start_date) & (data['fecha'] <= end_date)]
        except:
            pass

    if day_selected:
        data = data[data['ruta'].apply(lambda x: x in day_selected)]

    if hour_picked:
        data = data[data['hora'].apply(lambda x: float(x) in hour_picked)]

    #data = add_loads(data)
    return go.Figure(
        data=[
            map_links(df_full)  # Plot all streets
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),
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


@app.callback(
    Output("histogram-prediccion", "figure"),
    [Input("limpiar-prediccion", "n_clicks")],
)
def update_click_output(button_click):
    x = np.random.randn(500)
    return go.Figure(
                    data=[
                        go.Histogram(x=x)
                        ],
                    layout=go.Layout(
                                paper_bgcolor="white",
                                plot_bgcolor="white",
                                title="TITULO_AQUI"
                                )
                    )


#
# # LAYOUT DASH APP
#


app.layout = html.Div(
    children=[build_banner(),
              html.Div(
                  id='app-container',
                  children=[build_tabs(), html.Div(id='app-content')]),
              generate_modal()]
        )

if __name__ == '__main__':
    app.run_server(debug=True)
#     app.run_server(host='0.0.0.0')


# -----------------------------------------------------------
# demonstrates how to write ms excel files using python-openpyxl
#
# (C) 2015 Frank Hofmann, Berlin, Germany
# Released under GNU Public License (GPL)
# email frank.hofmann@efho.de
# -----------------------------------------------------------
