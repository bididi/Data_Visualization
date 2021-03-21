import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('database.csv')
df.dropna(inplace=True)
# print(pd.isnull(df).sum())
# df.index = pd.to_datetime(df['Date'])


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crime analize"
OptionsListe = [{"label": year, "value": year} for year in np.sort(df.Year.unique())]
OptionsListe.insert(0, {"label": "All", "value": 'all'}),
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Crimes Analytics", className="header-title"
                ),
                html.P(
                    children="Analyse crimes by year",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.P(children="kujyhgtrfedzsxwlkiujyhgtrfedzs ikjuhy-gtfredjuhygtrfd", className="data1")
                    ]
                ),
                html.Div(
                    children=[
                        html.P(children="kujyhgtrfedzsxwlkiujyhgtrfedzs ikjuhy-gtfredjuhygtrfd", className="data2")
                    ]
                ),
                html.Div(
                    children=[
                        html.P(children="kujyhgtrfedzsxwlkiujyhgtrfedzs ikjuhy-gtfredjuhygtrfd", className="data3")
                    ]
                )

            ],
            className="global_container"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Year", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=OptionsListe,
                            value='all',
                            clearable=False,
                            placeholder="Select a year",
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="fig", config={"displayModeBar": False},
                            ),
                            className="card",
                        )

                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="fig2", config={"displayModeBar": False},
                            ),
                            className="card",
                        )

                    ],
                ),

            ],
            className="Year_container"
        ),
        """html.Div(
            children=mapp
            classname="map_container"
        ),
        
        """
    ]
)


@app.callback(
    Output("fig", "figure"),
    Input("year-filter", "value"),

)
def update_charts(year):
    if year == "all":
        fig = go.Figure()
        fig.add_trace(go.Histogram(histfunc="count", x=df['Victim_Sex']))
    else:
        filtered_df = df[df.Year == year]
        fig = go.Figure()
        fig.add_trace(go.Histogram(histfunc="count", x=filtered_df['Victim_Sex']))
    return fig


#def crime_solved(year):
    #if year == 'all':
        #unsolved = df[df["Crime Solved"] != "Yes"]
        #solved = df[df["Crime Solved"] == "Yes"]
        #fig2 = go.Figure()
        #unsolved['Year'].value_counts().sort_index(ascending=True).plot(kind='line', label='Unsolved')
        #solved['Year'].value_counts().sort_index(ascending=True).plot(kind='line', label='Solved')
        #plt.legend()
        #plt.title('Solved/Unsolved crimes')
    #return plt

if __name__ == "__main__":
    app.run_server(debug=True)
