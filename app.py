import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df = pd.read_csv('database.csv')
df.dropna(inplace=True)
# print(pd.isnull(df).sum())
# df.index = pd.to_datetime(df['Date'])
nbr_crime = df['Record_ID'].count()
#print(nbr_crime)
unsolved = len(df[df["Crime_Solved"] != "Yes"])
solved = len(df[df["Crime_Solved"] == "Yes"])
Total = unsolved+solved
Mean = (solved/Total)*100
print(Mean)
Mean = round(Mean,2)
Weapon = df["Weapon"].value_counts().idxmax()
#print(Weapon)
Mean =str(Mean)
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
                        html.H3(children="Number crimes", className="header-title"),
                        html.P(children=nbr_crime)
                    ], className="data1"
                ),
                html.Div(
                    children=[
                        html.H3(children="Most popular weapon", className="header-title"),
                        html.P(children=Weapon)
                    ], className="data2"
                ),
                html.Div(
                    children=[
                        html.H3(children="Solved crimes", className="header-title"),
                        html.P(children=Mean + " % ")
                    ], className="data3"
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

                        ),
                    ],
                    className="dropdown"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="fig", config={"displayModeBar": False},
                            ),

                        )

                    ],
                    className="card1"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=dcc.Graph(
                                id="fig2", config={"displayModeBar": False},
                            ),

                        )

                    ],
                    className="card2"
                ),

            ],
            className="Year_container"
        ),
        """html.Div(
            children=mapp
            classname="map_container"
        ),
        
        """
    ],
    className="container"
)


@app.callback(
    Output("fig", "figure"),
    Input("year-filter", "value"),

)
def pie_chart(year):
    if year == "all":
        fig = px.pie(df,values="Year",names='Victim_Sex')
    else:
        filtered_df = df[df.Year == year]
        fig = px.pie(filtered_df,values="Year",names='Victim_Sex')
    return fig

def update_charts(year):
    if year == "all":
        fig2 = go.Figure2()
        fig2.add_trace(go.Histogram(histfunc="count", x=df['Victim_Sex']))
    else:
        filtered_df = df[df.Year == year]
        fig2 = go.Figure2()
        fig2.add_trace(go.Histogram(histfunc="count", x=filtered_df['Victim_Sex']))
    return fig2

#def crime_solved(year):
    #if year == 'all':

        #fig2 = go.Figure()
        #unsolved['Year'].value_counts().sort_index(ascending=True).plot(kind='line', label='Unsolved')
        #solved['Year'].value_counts().sort_index(ascending=True).plot(kind='line', label='Solved')
        #plt.legend()
        #plt.title('Solved/Unsolved crimes')
    #return plt

if __name__ == "__main__":
    app.run_server(debug=True)
