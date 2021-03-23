# Importations du projet

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

# Load data on our CSV
df = pd.read_csv('database.csv')
# We replace the null values
df.dropna(inplace=True)

# print(pd.isnull(df).sum())
# df.index = pd.to_datetime(df['Date'])

#We calculate the percentage of crime solved
nbr_crime = df['Record_ID'].count()
unsolved = len(df[df["Crime_Solved"] != "Yes"])
solved = len(df[df["Crime_Solved"] == "Yes"])
Total = unsolved + solved
Mean = (solved / Total) * 100
print(Mean)
Mean = round(Mean, 2)
# We are looking for the most used weapon
Weapon = df["Weapon"].value_counts().idxmax()
Mean = str(Mean)

# To create the map, we need to replace the state names by their abbreviation
df[["State"]] = df[["State"]].replace({'Alabama': 'AL',
                                       'Alaska': 'AK',
                                       'Arizona': 'AZ',
                                       'Arkansas': 'AR',
                                       'California': 'CA',
                                       'Colorado': 'CO',
                                       'Connecticut': 'CT',
                                       'Delaware': 'DE',
                                       'District of Columbia': 'DC',
                                       'Florida': 'FL',
                                       'Georgia': 'GA',
                                       'Hawaii': 'HI',
                                       'Idaho': 'ID',
                                       'Illinois': 'IL',
                                       'Indiana': 'IN',
                                       'Iowa': 'IA',
                                       'Kansas': 'KS',
                                       'Kentucky': 'KY',
                                       'Louisiana': 'LA',
                                       'Maine': 'ME',
                                       'Maryland': 'MD',
                                       'Massachusetts': 'MA',
                                       'Michigan': 'MI',
                                       'Minnesota': 'MN',
                                       'Mississippi': 'MS',
                                       'Missouri': 'MO',
                                       'Montana': 'MT',
                                       'Nebraska': 'NE',
                                       'Nevada': 'NV',
                                       'New Hampshire': 'NH',
                                       'New Jersey': 'NJ',
                                       'New Mexico': 'NM',
                                       'New York': 'NY',
                                       'North Carolina': 'NC',
                                       'North Dakota': 'ND',
                                       'Ohio': 'OH',
                                       'Oklahoma': 'OK',
                                       'Oregon': 'OR',
                                       'Pennsylvania': 'PA',
                                       'Rhodes Island': 'RI',
                                       'South Carolina': 'SC',
                                       'South Dakota': 'SD',
                                       'Tennessee': 'TN',
                                       'Texas': 'TX',
                                       'Utah': 'UT',
                                       'Vermont': 'VT',
                                       'Virginia': 'VA',
                                       'Washington': 'WA',
                                       'West Virginia': 'WV',
                                       'Wisconsin': 'WI',
                                       'Wyoming': 'WY'})
# We create a column of 1 to count the number of crimes
new_df = df.assign(Crime=1)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
#Launching the dashboard

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crime analize"
OptionsListe = [{"label": year, "value": year} for year in np.sort(df.Year.unique())]
OptionsListe.insert(0, {"label": "All", "value": 'all'}),
#Creation of the different boxes of our dashboard
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    #title
                    children="Crimes Analytics", className="header-title"
                ),
                html.P(
                    #Sub-title
                    children="Analyse crimes by year",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # The div with 3 global variable
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3(children="Number crimes", className="header-title"),
                        html.P(children=nbr_crime)
                    ], className="data"
                ),
                html.Div(
                    children=[
                        html.H3(children="Most popular weapon", className="header-title"),
                        html.P(children=Weapon)
                    ], className="data"
                ),
                html.Div(
                    children=[
                        html.H3(children="Solved crimes", className="header-title"),
                        html.P(children=Mean + " % ")
                    ], className="data"
                )

            ],
            className="global_container"
        ),
        html.Div(
            children=[
                html.Div(
                    # Our dropdown where we choose year
                    children=[
                        html.H2(children="Choose a year", className="menu-title"),
                        dcc.Dropdown(
                            id="year-filter",
                            options=OptionsListe,
                            value='all',
                            clearable=False,
                            placeholder="Select a year",

                        ),
                        html.H3(
                            children='Most popular weapon',
                            className="texte"

                        ),
                        html.P(
                            id="weapon",
                            className="chiffre"

                        ),
                        html.H3(
                            children='Number of crimes',
                            className = "texte"

                        ),
                        html.P(
                            id="crime",
                            className="chiffre"

                        ),
                        html.H3(
                            children='Pourcentage of solved crimes',
                            className="texte"

                        ),
                        html.P(
                            id="Solved",
                            className="chiffre"

                        ),
                        html.H3(
                            children='Average age of victims',
                            className="texte"

                        ),
                        html.P(
                            id="relation",
                            className="chiffre"

                        ),
                    ],
                    className="dropdown"
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="fig", config={"displayModeBar": False},
                                    ),
                                    className="card1",
                                ),
                                html.Div(
                                    children=dcc.Graph(
                                        id="fig2", config={"displayModeBar": False}
                                    ),
                                    className="card2",
                                ),

                            ],
                            className="graphs",
                        ),
                        html.Div(
                            children=dcc.Graph(
                                id="map", config={"displayModeBar": False},
                            ),
                            className="map_container"
                        ),

                    ],
                    className="droite"

                ),


            ],
            className="bbody"

        ),


    ],
    className="container"
)


@app.callback(
    Output("fig", "figure"),
    Output("fig2", "figure"),
    Output("weapon", "children"),
    Output("crime", "children"),
    Output("Solved", "children"),
    Output("relation", "children"),
    Output("map", "figure"),
    Input("year-filter", "value"),

)

#Method that allows us to display graphs with statistics year by year or with all the years.
#It returns all the graphs and variables of our dashboard
def pie_chart(year):
    if year == "all":
        # pie parameters
        fig = px.pie(df, values="Year", names='Victim_Sex')
        fig.update_layout(
            title="<b>Genders of the victims</b>",
            title_font_family="sans serif",
            title_font_size=25,
            font=dict(
                color="black"
            )
               )
        # histogram parameters
        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(histfunc="count", x=df['Month']))
        fig2.update_layout(
            title="<b>Histogram of crimes by month</b>",
            title_font_family="sans serif",
            title_font_size=25,
            font=dict(
                color="black"
            )
        )
        # return the most usefull arms
        weapon = df["Weapon"].value_counts().idxmax()
        # returns the average age of victims
        relation = df["Victim_Age"].mean()
        relation = round(relation, 2)

        crime = df['Record_ID'].count()
        #Allows to make the percentage of crime solved according to the year
        Unsolved = len(df[df["Crime_Solved"] != "Yes"])
        solve = len(df[df["Crime_Solved"] == "Yes"])
        total = Unsolved + solve
        mean = (solve / total) * 100
        mean = round(mean, 2)
        Solved = str(mean)

        new_df1 = new_df.groupby(by=["State"]).sum()
        new_df1.reset_index(level=0, inplace=True)
        # map parameters
        map = px.choropleth(
            data_frame=new_df1,
            locationmode='USA-states',
            locations=new_df1["State"],
            scope="usa",
            color_continuous_scale="Reds",
            color='Crime',
            title='<b>Distribution of crimes by state, in the USA</b>',
            hover_data=['State', 'Crime'],

        )
        map.update_layout(
            title_font_family="sans serif",
            title_font_size=25,
            font=dict(
                color="black"
            )
        )
    else:
        # new dataframe with years by years
        filtered_df = df[df.Year == year]
        filtered_df2 = new_df[new_df.Year == year]

        new_df2 = filtered_df2.groupby(by=["State"]).sum()
        new_df2.reset_index(level=0, inplace=True)
        # returns the most used weapon
        weapon = filtered_df["Weapon"].value_counts().idxmax()
        #returns the average victim
        relation = filtered_df["Victim_Age"].mean()
        relation = round(relation, 2)

        crime = filtered_df['Record_ID'].count()
        #pie parameters
        fig = px.pie(filtered_df, values="Year", names='Victim_Sex')
        fig.update_layout(
            title="<b>Genders of the victims</b>",
            title_font_family="sans serif",
            title_font_size=25,
            font=dict(
                color="black"
            )
        )
        fig2 = go.Figure()
        # histogram parameters
        fig2.add_trace(go.Histogram(histfunc="count", x=filtered_df['Month']))
        fig2.update_layout(
            title="<b>Histogram of crimes by month</b>",
            title_font_family="sans serif",
            title_font_size=25,
            font=dict(
                color="black"
            ))
        Unsolved = len(filtered_df[filtered_df["Crime_Solved"] != "Yes"])
        solve = len(filtered_df[filtered_df["Crime_Solved"] == "Yes"])
        total = Unsolved + solve
        mean = (solve / total) * 100
        mean = round(mean, 2)
        Solved = str(mean)
        Solved = Solved
        # map parameters
        map = px.choropleth(
            data_frame=new_df2,
            locationmode='USA-states',
            locations=new_df2["State"],
            scope="usa",
            color_continuous_scale="Reds",
            color='Crime',
            hover_data=['State', 'Crime'],
            range_color=(0, 3000),
            title="<b>Distribution of crimes by state, in the USA</b>",

        )

    return fig, fig2, weapon, crime, Solved, relation,map


if __name__ == "__main__":
    app.run_server(debug=True)
