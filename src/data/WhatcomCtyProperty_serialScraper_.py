# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:04:44 2021

@author: Varun.Ramesh
"""

##On analysis of parallely scraped data several outputs were found missing that were available in the data. 
#These links were scrapped serially. 

import pandas as pd
import helper_functions
from itertools import combinations,cycle, islice
import pathos.multiprocessing as mp
from selenium import webdriver
import time

#read dataframe
df_part2 = pd.read_csv('Bellingham_Property_Part2.csv', index_col=[0])

#find missing links
df_part2_missingvals = df_part2.loc[(df_part2.Neighborhood=='0'),:]

#unique id of missing links used for scraped
links_missing_vals = df_part2_missingvals['Unique ID'].values.tolist()

#create a worker
worker = helper_functions.create_worker()

result = []

link_number = 0

#scrape data. Note I started multiple instances of python and scraped various lengths of the links on different consoles to make processing faster.
for link in links_missing_vals[9200:]:
    link_number+=1
    start = time.time()
    result.append(helper_functions.scrape_website(link,worker))
    print('Completed processing {} of {} chunks in {} secs'.format(link_number,len(links_missing_vals),(time.time() - start)))

#load results in dataframe
df = pd.DataFrame(result,columns = ['Sale Date','assesors_link','Neighborhood', 'Land Acres','Built Sq ft','bedroom','bathroom','year_built'])

#send to csv
df.to_csv('console5_data.csv')   

#It is a mystery why the data is available with serial scraping and not parallel scraping. 