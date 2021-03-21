import json
import requests
import pandas as pd

#Seattle Crime data
url = "https://data.seattle.gov/resource/tazs-3rd5.json?$limit=900000&$offset=0&$order=offense_id"

output_folder = 'D:\\OneDrive - PACCAR Inc\\Current_Projects\\Personal\\Courses\\DataScientist\\Project 1\\cov2_crimerate\\data\\raw\\'

def api_json_to_pandas(url):
    r = requests.get(url)
    json_data = r.json()
    df = pd.json_normalize(json_data)
    return df

if __name__ == '__main__':
   seattle_crime_data=api_json_to_pandas(url)
   seattle_crime_data.to_csv(output_folder+'Seattle_Crime_Data.csv')





