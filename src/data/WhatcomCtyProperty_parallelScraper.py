# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:58:12 2021

@author: Varun.Ramesh
"""
import pandas as pd
import helper_functions
from itertools import combinations,cycle, islice
import pathos.multiprocessing as mp
from selenium import webdriver
import time

def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]

#Read list of propery sales to be scraped
df_part1 = pd.read_csv('Bellingham_Property_Part1.csv', index_col=[0])

#create empty dataframe to store property information
df_part2 = pd.DataFrame(columns = ['Sale Date', 'assesors_link','Neighborhood', 'Land Acres','Built Sq ft','bedroom','bathroom','year_built'])  

p = mp.ProcessingPool(mp.cpu_count()) #use pathos for multi-processing
total_chunks = 1000 #split dataset into 1000 chunks processed in parallel
chunked_links = chunks(assesors_link,total_chunks); #list of chunked links

chunk_number = 0

for out in chunked_links: #process links in chunks
    chunk_number+=1   
    start = time.time()
    df = pd.DataFrame(p.map(helper_functions.scrape_website, out),columns = ['Sale Date','assesors_link','Neighborhood', 'Land Acres','Built Sq ft','bedroom','bathroom','year_built'])
    df_part2 = pd.concat([df_part2,df],axis =0)
    print('Completed processing {} of {} chunks in {} secs'.format(chunk_number,total_chunks,(time.time() - start)))
          
#unique id is used to join
df_part2['Unique ID'] = [ x+'_sep_'+y for x,y in zip(df_part2['Sale Date'].tolist(),df_part2['assesors_link'].tolist())]

#write output to csv
df_part2.to_csv('Bellingham_Property_Part2.csv')   
              
df_combined = df_part1.set_index('Unique ID').join(df_part2.set_index('Unique ID'),lsuffix='_part1', rsuffix='_part2')

#export dataframe to cvs
df_combined.to_csv('Bellingham_Property_Sale_Combined.csv')            
    