import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load data
df = pd.read_csv('database.csv')
df.dropna(inplace=True)
#print(pd.isnull(df).sum())
#df.index = pd.to_datetime(df['Date'])


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

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
                        html.Div(children="Year", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {"label": year, "value": year}
                                for year in np.sort(df.Year.unique())
                            ],
                            value=2010,
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                )
            ],
            className="menu",
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
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("fig", "figure"),
    Input("year-filter", "value")

)
def update_charts(year):

    filtered_df = df[df.Year == year]
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=filtered_df['Victim_Sex']))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
