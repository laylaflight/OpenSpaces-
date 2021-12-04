import pandas as pd 
import streamlit as lt
import plotly.express as px
from geopy.geocoders import Nominatim


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

def process():
    # https://www.webfx.com/tools/emoji-cheat-sheet/
    lt.set_page_config(page_title="Covid-19 Hospitalizations and Deaths",
                    page_icon=":chart_with_upwards_trend:",
                    layout="wide",
    )
    file1 = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    file2 = "Open_Streets_Locations.csv"
    df = get_data(file1)

    title = "Open Spaces"
    title_color = "green"
    description = """
    A way to show the rise of covid cases that ultimately lead to New York City's push for more open spaces for bicyclists and pedestrians. Depicting the new pathways for pedestrians and cyclists to practice social distancing.
    """
    lt.markdown("<h1 style='text-align: center; color: " + title_color + "'>" + title + "</h1><div>" + description + "</div>", unsafe_allow_html=True)
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

    geo_left.plotly_chart(fig5)
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