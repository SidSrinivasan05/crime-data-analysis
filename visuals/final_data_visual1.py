import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from phase2_data_cleaning.api_data_collect import api_web_parser

dfApi = api_web_parser() 
dfApi = dfApi.reset_index()
dfApi = dfApi.drop(['index', 'footnote_codes', 'id', 'year', 'period', 'area_code', 'area_text', 'series_id', 'month'], axis=1)
dfApi.columns = ['values', 'series_title', 'dates']


dfWeb = pd.read_csv('phase2_data_cleaning/cleaned_webscrapped_data.csv')
dfWeb['series_title'] = pd.Series(index=dfWeb.index).fillna('(Seas) Labor Force Participation Rate')
dfWeb['dates'] = dfWeb['date']
dfWeb = dfWeb.drop(['Unnamed: 0', 'period', 'date'], axis=1)

# # Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=dfApi['dates'], y=dfApi['values'], name="Employment: Atlanta city, GA (U)"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=dfWeb['dates'], y=dfWeb['values'], name="Labor Force Participation Rate"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Atlanta Employment vs US Labor Force Participation Rate"
)

# Set x-axis title
fig.update_xaxes(title_text="Time")

# Set y-axes titles
fig.update_yaxes(title_text="Employment Rate", secondary_y=False)
fig.update_yaxes(title_text="Participation Rate", secondary_y=True)

fig.show()

# dual_line_graph
# visualization ^
