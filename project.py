from enum import auto
import pandas as pd 
import streamlit as lt
import plotly.express as px
import json
import math
from geopy.geocoders import Nominatim
import numpy as np
from sklearn import neighbors
from PIL import Image


#NAME: Layla Flight
#EMAIL: layla.flight01@myhunter.cuny.edu
#TITLE: Open Spaces 
#RESOURCES: Tutor-Frank Y; youtu.be/Sb0A9i6d320; askpython.com/python/examples/plot-geographical-data-python-plotly;towardsdatascience.com/pythons-geocoding-convert-a-list-of-addresses-into-a-map-f522ef513fd6; discuss.streamlit.io/t/how-to-set-the-background-body-color-of-streamlit-complete-app/3879;blog.streamlit.io/introducing-theming/
#URL: share.streamlit.io/laylaflight/openspaces-/main/project.py


def getLatLon():
    nycData = {}
    geolocator = Nominatim(user_agent="example app")
    geoData = [
                ["SI_NY", geolocator.geocode("Staten Island, NY").raw],
                ["BX_NY", geolocator.geocode("Bronx, NY").raw],
                ["BK_NY", geolocator.geocode("Brooklyn, NY").raw],
                ["QN_NY", geolocator.geocode("Queens, NY").raw],
                ["MN_NY", geolocator.geocode("Manhattan, NY").raw],
    ]
    for item in geoData:
        nycData[item[0]] = [item[1]['lat'], item[1]['lon']]
    return nycData

@lt.cache
def get_data(file1):
    df = pd.read_csv(file1)
    df.index = pd.to_datetime(df['DATE_OF_INTEREST'], format="%m/%d/%Y", errors='coerce') 
    df.groupby(by=[df.index.year, df.index.month])
    
    return df 

def NYCMap():
    # load geojson data for manhattan
    nycmap = json.load(open("nycpluto_manhattan.geojson"))

    # load library data from csv file, convert coordinates to radians, and create coordinate pairs
    libs = pd.read_csv('manhattanlibraries.csv', usecols=['facname', 'latitude', 'longitude'])
    libs['latitude'] = libs['latitude'].apply(func=math.radians)
    libs['longitude'] = libs['longitude'].apply(func=math.radians)
    libs['coord'] = list(zip(libs['latitude'], libs['longitude']))

    # load library data into BallTree
    libcoords = np.asarray(list(libs['coord']))
    tree = neighbors.BallTree(libcoords, metric="haversine")

    # load lot data from csv file, convert coordinates to radians, and create coordinate pairs
    df = pd.read_csv('pluto_small.csv')
    df = df.dropna(subset=['assesstot', 'bldgarea', 'lotarea', 'latitude', 'longitude'])
    df['latitude'] = df['latitude'].apply(func=math.radians)
    df['longitude'] = df['longitude'].apply(func=math.radians)
    df['coord'] = list(zip(df['latitude'], df['longitude']))

    # query the BallTree and save results back in df
    lotcoords = np.asarray(list(df['coord']))
    dist, _ = tree.query(X=lotcoords, k=1)
    df['dist'] = dist
    df['dist'] = df['dist'].apply(lambda x: x*3960)

    # use Plotly express function to create a choropleth map
    fig = px.choropleth_mapbox(df,
                            geojson=nycmap,
                            locations="bbl",
                            featureidkey="properties.bbl",
                            color="dist",
                            color_continuous_scale=px.colors.sequential.thermal[::-1],
                            range_color=(0, 0.5),
                            mapbox_style="carto-positron",
                            zoom=9, center={"lat": 40.7, "lon": -73.7},
                            opacity=0.7,
                            hover_name="ownername"
                            )

    fig.update_layout(title_text="NYC Open Space Locations ", title_x=0.5, autotypenumbers='convert types')
    #fig.show()
    return fig

def process():
    # https://www.webfx.com/tools/emoji-cheat-sheet/
    lt.set_page_config(page_title="Covid-19 Hospitalizations and Deaths",
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide",
    )
    file1 = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    file2 = "Open_Streets_Locations.csv"
    df = get_data(file1)

    lt.markdown("""
    <style>
    .big-font {
        font-size:100px !important;
        text-align: center;
        color:green;
        font-family: "Papyrus", fantasy;
    }
    .p3{
        font-size:30px;
        font-family: "Papyrus", fantasy;
    }
    .p2{
        font-size:20px;
        font-family: "Papyrus", fantasy;
    }
    </style>
    """, unsafe_allow_html=True)
    lt.markdown('<p class="big-font">Open Spaces !!</p>', unsafe_allow_html=True)
    image = Image.open('bicycle.png')
    lt.image(image ,width=60, use_column_width=auto, clamp=False, channels="RGB", output_format="auto")
    lt.markdown('<p class="p2">Created by: Layla Flight</p>', unsafe_allow_html=True)
    lt.markdown('<p class="p3">A way to show the rise of covid cases that ultimately lead to New York City push for more open spaces for bicyclists and pedestrians. Depicting the new pathways for pedestrians and cyclists to practice social distancing.</p>', unsafe_allow_html=True)
    lt.info('My hypothesis: When I first started this, I intended to show the growth of the covid cases during 2020. In addition to that,  the differences between the covid cases in each borough . Due to the pandemic , there were more open street locations so I wanted to show one of the better things that came out of such tragic times. With this in mind I used the nyc data from the Open Street Locations and Covid 19 Daily Count of Cases. Also, used outside data sources of neighborhoods and areas in manhattan. I used tools such as streamlit to display everything and plotly for the tables. I was able to discover that the boroughs that had the overall highest hospitalizations and deaths were in brooklyn and queens. The bronx being right under brooklyn and manhattan soon following. The one with the least hospitalizations was staten island as a borough. The deaths seperated by boroughs giving the same result.    ')
    lt.info('Data: As mentioned before I used plotly.express to display the line graphs shown. For the first data set, it uses the data from Covid 19 Daily Count of Cases csv file. It was grouped by the hospitalization in the data set by each borough in NYC. Each borough seperated by each legend of a different color. For the second data set it is grouped by all boroughs representing hospitalizations in NYC . All denoted by one legend with the color of blue. The third data set is grouped by deaths from the Covid 19 csv and also seperated by borough. Similar to the second data set , the fourth data set shows all the boroughs and grouped by deaths from covid. For the open space locations csv , I used a map to show all the locations in the city .')
    lt.info('Techniques: When going through the process of creating this project , I used streamlit to create the aesthetics of the webpage. Within this I used some CSS elements and custom themes from streamlit. For the actual data sets I used pandas and plotly to create line graphs. The Plotly library has a wide selection when it comes to creating graphs. For the NYC map I used a choropleth mapbox to show the different locations by varying in color. The open space locations by the street column csv were converted into latitude and longitude that the map needed for the exact location so the map could be accurate. To work with map and accurate locations , I worked with geopy and geolocator to read in the components needed for the location the json and math libraries were used. ')
    lt.info('Citations:Tutor: Frank Y; youtu.be/Sb0A9i6d320; askpython.com/python/examples/plot-geographical-data-python-plotly;towardsdatascience.com/pythons-geocoding-convert-a-list-of-addresses-into-a-map-f522ef513fd6; discuss.streamlit.io/t/how-to-set-the-background-body-color-of-streamlit-complete-app/3879;blog.streamlit.io/introducing-theming/;')

    #city = lt.sidebar.multiselect('Select a Date Range:',
    #                              options = df['DATE_OF_INTEREST'].unique(),
    #                              default = df['DATE_OF_INTEREST'].unique(),
    #)
    title1 = "Hospitalizations by Borough in NYC"
    title2 = "Deaths by Borough in NYC"
    title3 = "Hospitalizations in NYC"
    title4 = "Deaths in NYC"
    #print(df)
    #df = df1.groupby(pd.Grouper(freq="M"))
    df_long1 = pd.melt(df, id_vars=['DATE_OF_INTEREST'], value_vars=['MN_HOSPITALIZED_COUNT', 'BX_HOSPITALIZED_COUNT', 'BK_HOSPITALIZED_COUNT', 'SI_HOSPITALIZED_COUNT', 'QN_HOSPITALIZED_COUNT'])
    fig1 = px.line(df_long1, x="DATE_OF_INTEREST", y='value', color='variable', labels={"value": "Hospitalizations", "variable": "Legend", "DATE_OF_INTEREST": "Date"})
    fig1.update_layout(title_text=title1, title_x=0.5)
    #fig1.show()
    df_long2 = pd.melt(df, id_vars=['DATE_OF_INTEREST'], value_vars=['MN_DEATH_COUNT', 'BX_DEATH_COUNT', 'BK_DEATH_COUNT', 'SI_DEATH_COUNT', 'QN_DEATH_COUNT'])
    fig2 = px.line(df_long2, x="DATE_OF_INTEREST", y='value', color='variable', labels={"value": "Deaths", "variable": "Legend", "DATE_OF_INTEREST": "Date"})
    fig2.update_layout(title_text=title2, title_x=0.5)
    #fig2.show()

    df_long3 = pd.melt(df, id_vars=['DATE_OF_INTEREST'], value_vars=['HOSPITALIZED_COUNT'])
    fig3 = px.line(df_long3, x="DATE_OF_INTEREST", y='value', color='variable', labels={"value": "Hospitalizations", "variable": "Legend", "DATE_OF_INTEREST": "Date"})
    fig3.update_layout(title_text=title3, title_x=0.5, autotypenumbers='convert types')
    #fig3.show()
    df_long4 = pd.melt(df, id_vars=['DATE_OF_INTEREST'], value_vars=['DEATH_COUNT'])
    fig4 = px.line(df_long4, x="DATE_OF_INTEREST", y='value', color='variable', labels={"value": "Deaths", "variable": "Legend", "DATE_OF_INTEREST": "Date"})
    fig4.update_layout(title_text=title4, title_x=0.5)
    #fig4.show()
    latLong = getLatLon()
    df['lon'] = latLong["QN_NY"][1]
    df['lat'] = latLong["QN_NY"][0]
    df['Name'] = 'Bronx'
    fig5 = px.scatter_geo(df, 
                          lon="lon",
                          lat="lat",
                          projection="natural earth",
                          hover_name="Name",
                          hover_data = {
                                    "Name": False,
                                    "lon": False,
                                    "lat": False
                          },
                          #scope='usa',
                          #width=300,
                          #height=100,
                          )
    
    #fig5.update_layout(
    #                geo = dict(projection_scale=200,
    #                        center=dict(lat=float(df['lat'][0]), lon=float(df['lon'][0]))
    #                )
    #)
    left_column, right_column = lt.columns(2)
    left_column.plotly_chart(fig1)
    right_column.plotly_chart(fig3)

    left_column, right_column = lt.columns(2)
    left_column.plotly_chart(fig2)
    right_column.plotly_chart(fig4)

    geo_left,geo_right = lt.columns(2)

    print(dir(geo_left))
    print(dir(geo_left.plotly_chart))
    geo_left.plotly_chart(NYCMap())
    #lt.plotly_chart(fig1)
    #lt.plotly_chart(fig2)
    #lt.plotly_chart(fig3)
    #lt.plotly_chart(fig4)

    #fig.add_scatter(x=df['DATE_OF_INTEREST'], y=['SI_HOSPITALIZED_COUNT'], mode='lines')
    #fig.add_scatter(x=df['DATE_OF_INTEREST'], y=['BX_HOSPITALIZED_COUNT'], mode='lines')
    #fig.add_scatter(x=df['DATE_OF_INTEREST'], y=['BK_HOSPITALIZED_COUNT'], mode='lines')
    #fig.add_scatter(x=df['DATE_OF_INTEREST'], y=['QN_HOSPITALIZED_COUNT'], mode='lines')

process()
#print(getLatLon())