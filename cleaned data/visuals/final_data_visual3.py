import plotly.express as px
import pandas as pd
import numpy as np

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


droplist = []
for i in dfCrime.index:
    if dfCrime.loc[i,'Occur Date'] is None:
        droplist.append(i)
    elif int( dfCrime.loc[i,'Occur Date'].split('-')[0] ) < 2009:
        droplist.append(i)
    elif int( dfCrime.loc[i,'Occur Date'].split('-')[0] ) > 2024:
        droplist.append(i)

dfCrime = dfCrime.drop(droplist, axis=0)

stats = dfCrime.groupby(["Occur Date", "Crime Type"])["Report Number"].count().reset_index()
stats.columns = ["Occur Date", "Crime Type", "Number of Crimes Committed"]
stats['Occur Date'] = np.array(stats['Occur Date'], dtype='datetime64[D]')

stats['Occur Date'] = np.array(stats['Occur Date'], dtype='datetime64[D]')
stats['Year'] = pd.Series(stats['Occur Date']).apply( lambda x : x.year )

fig = px.scatter(stats, x="Occur Date", y="Number of Crimes Committed", color="Crime Type", title='Non-Violent vs Violent Crimes in Atlanta'
                    , labels={"Occur Date": "Years"})

fig.show()
