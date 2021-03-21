from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options


def create_worker():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')    
    worker = webdriver.Chrome(executable_path='D:/Tools/MyTools/Drivers/chromedriver.exe',chrome_options=chrome_options)
    return worker


def scrape_website(url,worker):
    sale_date = url.split('_sep_')[0]
    link = url.split('_sep_')[1]
    worker.get('https://property.whatcomcounty.us/PropertyAccess/'+link)
    sub_content = worker.page_source
    sub_content_soup = BeautifulSoup(sub_content,'html.parser')
    try:
        neighborhood = sub_content_soup.find("div", {"id": "propertyDetails"}).find(text = 'Neighborhood:').findNext('td').contents[0].__str__()
    except:
       neighborhood = '0' 
    try:
        land_acres= sub_content_soup.find("div", {"id": "propertyDetails"}).find(text = 'Legal Acres:').findNext('td').contents[0].__str__()
    except:
        land_acres = '0'
    try:
        built_sq_ft= sub_content_soup.find("div", {"id": "improvementBuildingDetails"}).find(text = 'State Code:').findNext('td').findNext('td').contents[0].__str__()
    except:
        built_sq_ft='0'
        bedroom='0'
        bathroom='0'
        year_built='0'
        return sale_date,link,neighborhood,land_acres,built_sq_ft,bedroom,bathroom,year_built             
    try:
        bedroom=sub_content_soup.find("div", {"id": "improvementBuildingDetails"}).find(text = 'Number of Bedrooms:').findNext('td').contents[0].__str__()
    except:
        bedroom='0'
    try:
        bathroom = 0
        baths=sub_content_soup.find("div", {"id": "improvementBuildingDetails"}).find_all(text = re.compile(r"Baths*"))
        for bath in baths:
            bathroom+=int(sub_content_soup.find("div", {"id": "improvementBuildingDetails"}).find(text = re.compile(bath)).findNext('td').contents[0])
        bathroom = str(bathroom)
    except:
        bathroom='0'
    try:
        year_built=sub_content_soup.find("table", class_='improvementDetails').find(text = re.compile(r"[0-9]{4}$")).__str__()
    except:
        year_built = '0'
    return sale_date,link,neighborhood,land_acres,built_sq_ft,bedroom,bathroom,year_built