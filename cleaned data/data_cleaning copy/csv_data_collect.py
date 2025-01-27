import csv
import pandas as pd

def csv_data_parser():
    with open('2009_2020CrimeData.csv', 'r') as file:
        f = csv.reader(file)
        readerList = [line for line in f]

    readerList[0][0] = 'IDCol' #The IDCol Column heading has some invisible strings, making it hard to reference

    df = pd.DataFrame( readerList[1:], columns=readerList[0] )

    df = df.sort_values(by=['Report Number'])
    df = df.reset_index()


    dropIndexes = []
    for i in df.index[1:]:
        if df.loc[i, 'Report Number'] == df.loc[i - 1, 'Report Number']:
            dropIndexes.append(i)

    df = df.drop(dropIndexes, axis = 0)
    df = df.drop(['index'], axis=1)


    for i in df.index:
        if df.loc[i, 'Occur Date'] == 'NULL':
            df.loc[i, 'Occur Date'] = df.loc[i, 'Report Date'].split()[0]

        if df.loc[i, 'Occur Time'] == 'NULL':
            df.loc[i, 'Occur Time'] = '12:00:00 AM'


        if df.loc[i, 'Possible Date'] == 'NULL':
            df.loc[i, 'Possible Date'] = df.loc[i, 'Report Date'].split()[0]

        if df.loc[i, 'Possible Time'] == 'NULL':
            df.loc[i, 'Possible Time'] = '12:00:00 AM'	

    df.to_csv('cleaned_atlantaCrime_csv_data.csv')
    return df

############ Function Call ############

print(csv_data_parser())