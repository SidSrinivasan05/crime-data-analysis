from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

import time

from bs4 import BeautifulSoup
import pandas as pd


def web_parser():

  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

  # Open Scrapingbee's website
  driver.get('https://data.bls.gov/dataViewer/view/timeseries/LNS11300000')
  start_year_dropdown = driver.find_element(By.TAG_NAME, 'select')
  select = Select( start_year_dropdown )
  select.select_by_visible_text('2008')

  update_button = driver.find_element(By.XPATH, '//*[@id="dv-submit"]')
  update_button.click()

  time.sleep(2)


  html = driver.page_source


  soup = BeautifulSoup(html , 'html.parser')
  data_value = soup.find('div', {'id' : 'bodytext'} ).find('div', {'id' : 'tablediv1'} ).find('tbody').find_all('td', {'class' : ""})
  data_time = soup.find('div', {'id' : 'bodytext'} ).find('div', {'id' : 'tablediv1'} ).find('tbody').find_all('td', {'class' : "abbrlabel"})
  data_period = soup.find('div', {'id' : 'bodytext'} ).find('div', {'id' : 'tablediv1'} ).find('tbody').find_all('td', {'class' : "period"})


  data_dictionary={}

  value_list = []
  time_list = []
  period_list = []

  for i in data_value:
      value_list.append(i.text.strip() )

  for j in data_time:
      time_list.append(j.text.strip() )

  for k in data_period:
      period_list.append(k.text.strip() )

  for item in range( len(value_list) ):
      data_dictionary[item] = [value_list[item], time_list[item], period_list[item]]
      
  for key in data_dictionary:
      data_dictionary[key][1] = f'{data_dictionary[key][1].split()[0]}-{data_dictionary[key][2][1:]}-01' 

  df = pd.DataFrame(data_dictionary, index=['values', 'date', 'period']).T 

  df.to_csv('cleaned_webscrapped_data.csv')

  return df





############ Function Call ############

print( web_parser())