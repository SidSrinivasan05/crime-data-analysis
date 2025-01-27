import plotly.express as px
import pandas as pd


def year_format(x):
    try:
        l = x.split('/')
        if len(l[1]) == 1:
            l[1] = '0' + l[1]
        if len(l[0]) == 1:
            l[0] = '0' + l[0]

        o = [l[2], l[0], l[1]]
        return ('-'.join(o) )
    except:
        a = x
def crime_type(x):
        if x in ['HOMICIDE', 'ROBBERY', 'AGG ASSAULT']:
            return 'VIOLENT'
        else:
            return 'NON-VIOLENT'

dfCrime = pd.read_csv('phase2_data_cleaning/cleaned_atlantaCrime_csv_data.csv')
dfCrime = dfCrime.drop(['Unnamed: 0'], axis=1)

dfCrime['Occur Date'] = pd.Series(dfCrime['Occur Date']).apply( lambda x : year_format(x) )
dfCrime['Crime Type'] = pd.Series(dfCrime['Crime Type']).apply( lambda x : crime_type(x) )

dfCrime['Latitude'] = dfCrime['Latitude'].round(3)
dfCrime['Longitude'] = dfCrime['Longitude'].round(3)

droplist = []
for i in dfCrime.index:
    if dfCrime.loc[i,'Occur Date'] is None:
        droplist.append(i)
    elif int( dfCrime.loc[i,'Occur Date'].split('-')[0] ) < 2009:
        droplist.append(i)
    elif int( dfCrime.loc[i,'Occur Date'].split('-')[0] ) > 2024:
        droplist.append(i)
    elif  dfCrime.loc[i,'Crime Type'] == 'NON-VIOLENT':
        droplist.append(i)

dfCrime = dfCrime.drop(droplist, axis=0)

fig = px.scatter_mapbox(
    dfCrime,
    lat="Latitude",
    lon="Longitude",
    color="Crime Type",
    hover_name="Neighborhood",
    hover_data={"Longitude": True, "Latitude": True, "Crime Type": True},
    title="Crime Distribution in Atlanta",
    mapbox_style="carto-positron",
    zoom=10,
    height=600,)
fig.show()