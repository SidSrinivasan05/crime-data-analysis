import requests
import pandas as pd

def api_web_parser(params=1):

	URL = 'https://sharefulton.fultoncountyga.gov/resource/5rm7-xueu.json?area_code='
	AREA_CODE = 'CT1304000000000'
	OFFSET = '&$offset=1099'

	response = requests.get(URL+AREA_CODE+OFFSET)

	df = pd.DataFrame(response.json() )

	df['value'] = df['value'].astype(float)
	df['year'] = df['year'].astype(int)
	df = df.sort_values(by='month2')

	droplist = []
	for i in df.index:
		if df.loc[i,'year'] < 2009:
			droplist.append(i)
		if df.loc[i,'series_id'] != 'LAUCT130400000000005':
			droplist.append(i)

	df = df.drop(droplist, axis=0)

 
	if params == 1:
		df.to_csv('cleaned_unemployment_api_data.csv')
 
	return df



############ Function Call ############
#print( api_web_parser() )