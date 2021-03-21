import pandas as pd
import helper_functions
from itertools import combinations,cycle, islice
import pathos.multiprocessing as mp
from selenium import webdriver
import time

#start driver. Chromium driver exec is located in path
driver = webdriver.Chrome(executable_path='D:/Tools/MyTools/Drivers/chromedriver.exe') #modify executable_path to where driver is located

##Navigate to https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx and 
##search for all residential sales between 2015 and 2021.

#Do no close the browser

#open window
driver.execute_script("window.open('https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx?cid=0&rtype=address&page=1');")

#start scraping for page 1 throughh 178 (or maximum on page)
pg_start = 1
pg_end = 178
current_page = 0

#initialize lists
address = []
sale_date = []
sale_price = []
built_sq_ft = []
bedroom =[]
assesors_link = []
bathroom = []
neighborhood = []
land_acres = []
year_built = []

while current_page <= pg_end:
    current_page += 1 #increment page
    
    #get page
    driver.get('https://property.whatcomcounty.us/PropertyAccess/SearchResultsSales.aspx?cid=0&rtype=address&page='
               +str(current_page))
    
    #read content
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')
    
    #parse through each table line
    for tr in soup.find_all('tr')[2:]:
        try: #read in property type (only accept residential property)
            prop_type = tr.find('td',class_="ss-prop-type").renderContents().strip().decode('utf-8')
        except:
            continue
        
        #only searching for homes in bellingham
        if prop_type == 'Real' and ('BELLINGHAM' in tr.find('td',class_="ss-situs").renderContents().strip().decode('utf-8')):
            address.append(tr.find('td',class_="ss-situs").renderContents().strip().decode('utf-8')) #popoulate address
            sale_date.append(tr.find('td',class_="ss-sale-date").renderContents().strip().decode('utf-8')) #populate sale date
            sale_price.append(tr.find('td',class_="ss-sale-price").renderContents().strip().decode('utf-8'))   #populate sale price         
            assesors_link.append(tr.find('td',class_="ss-view-property").find('a', href=True)['href'])  #populate assesors link

#create a datafrane and load lists into dataframe               
df = pd.DataFrame(list(zip(address,sale_date,sale_price,assesors_link)), 
               columns =['Address','Sale Date','Sale Price','assesors_link'])

#unique identifier for each proerpty id and sale date
df['Unique ID'] = [ x+'_sep_'+y for x,y in zip(pd.read_csv('Bellingham_Property_Part1.csv')['Sale Date'].tolist(),pd.read_csv('Bellingham_Property_Part1.csv')['assesors_link'].tolist())]

#export dataframe to cvs
df.to_csv('Bellingham_Property_Part1.csv')  