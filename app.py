import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('database.csv')
df.dropna(inplace=True)
print(pd.isnull(df).sum())
#df.index = pd.to_datetime(df['Date'])

app = dash.Dash(__name__)


app.layout = html.Div(
    children=[
        html.H1(children="Crimes Analytics",),
        html.P(
            children="Analyse crimes by year",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["Year"],
                        "y": df["Victim Count"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Incident per year"},
            },
        ),

    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
