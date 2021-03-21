import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

#Initialize Scraper
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
print('Scraping the Latest COB Police Activity Report...')

# first, use a get request
url = 'https://police.cob.org/PIRPressSummary/ReleaseForm.aspx'
r_get = requests.get(url, headers=headers)
data = r_get.text
soup = bs(data, 'lxml')

#Search Period - the form only support 3 months increments, we will limit to 1 month
#Tuple of start and end month for search e.g. (1,2) is (January, February)
FromToMonth = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,1)] 
#Tuple of start and end year incrementer for search corresponding to start and end month e.g. (0,1) is (2020, 2021)
FromToYear = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,1)] 
#list of years to query
Years = [2015,2016,2017,2018,2019,2020,2021] #list of years to search

#terms for re search 
#search for pattern in report
search_terms = [r'Reported: (\w+)',r'Location: (\w+)',r'Offense: (\w+)',r'Case #: (\w+)']
#split text based on string and get data
split_terms = ['Reported:','Location:',r'Offense:',r'Case #:']

#initialize lists
report_date = []
location = []
offence = []
case = []

#post form and process output in a loop of 1-month increment
for year in Years:
    counter= 0
    for month in FromToMonth:
        # our _EVENTTARGET is the search button
        postdata = {
            'ddlFromMonth':str(FromToMonth[counter][0]),
            'ddlFromDate':'1',
            'ddlFromYear':str(year+FromToYear[counter][0]),
            'ddlToMonth':str(FromToMonth[counter][1]),
            'ddlToDate':'1',
            'ddlToYear':str(year+FromToYear[counter][1]),
            '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'})['value'],
            '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value'],
            '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'})['value'],
            '__EVENTTARGET': 'btnGo',
        }
        counter+=1
        
        #post form and retrieve results using beautiful soup
        r_post = requests.post(url, data=postdata, cookies=r_get.cookies, headers=headers)
        soup = bs(r_post.text, 'html.parser')
        
        #extract data from table       
        for tr in soup.find_all('tr')[3:]:
            tds = tr.find('td')
            #Perform re search, split text and extract information
            for line in tds.text.splitlines():
                match_term=[]
                match = [re.search(search_term, line) for search_term in search_terms]
                
                #classify line as report data, location, offence, or case
                if not all(v is None for v in match):
                    match_term = next(i for i, j in enumerate(match) if j)
            
                if match_term == 0:
                    report_date.append(line.split(split_terms[match_term])[1].replace('\n',''))
                    
                if match_term == 1:
                    location.append(line.split(split_terms[match_term])[1].replace('\n',''))
                    
                if match_term == 2:
                    offence.append(line.split(split_terms[match_term])[1].replace('\n',''))
                
                if match_term == 3:
                    case.append(line.split(split_terms[match_term])[1].replace('\n',''))
         
            

#create a datafrane and load lists into dataframe               
df = pd.DataFrame(list(zip(report_date, location,offence,case)), 
               columns =['Date','Location','Offence','Case'])

#export dataframe to cvs
df.to_csv('COB_CrimeReport.csv')