#!/usr/bin/python

import re
import sys
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time
from stravalib.client import Client
import requests

def fetch_data(row,now):
    time.sleep(6)
    friend_name = row['name']
    url = requests.get('http://www.strava.com/athletes/'+str(row['id']))
    soup = BeautifulSoup(url.content, "html.parser")
    tables = soup.findAll('table')
    tablerows = tables[0].findAll('tr')
    for row in tablerows:
        if row.find('th').text == 'Distance':
            friend_distance_raw = row.find('td').text
            friend_distance = cleanconvert(friend_distance_raw)
    print(str(now)+'  :'+friend_name+' - '+str(friend_distance))
    output_string = str(now)+','+str(friend_name)+','+str(friend_distance)
    return(output_string)

def cleanconvert(friend_distance_raw):
    if re.search(r'km',friend_distance_raw):
        friend_distance_raw = friend_distance_raw[:-2]
        friend_distance_raw = re.sub("[^\d\.\-]", "", friend_distance_raw)
        friend_distance_raw = float(friend_distance_raw)
        friend_distance_raw = round(friend_distance_raw,1)
        
    elif re.search(r'mi',friend_distance_raw):
        friend_distance_raw = friend_distance_raw[:-2]
        riend_distance_raw = re.sub("[^\d\.\-]", "", friend_distance_raw)
        friend_distance_raw = float(friend_distance_raw) * 1.609344
        friend_distance_raw = round(friend_distance_raw,1)
    return(friend_distance_raw)

        
def main():

    friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)
   
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()

    outputlist = []
    
    #should try to redo this using apply:
    for index,row in friend_df.iterrows():        
        outputlist.append(fetch_data(row,now))
       
    
    outfile = open('distance.csv', 'a+')
    for s in outputlist:
        outfile.write(s)
        
        outfile.write('\n')
    print(str(now)+'  :  ACTION:    new data added to '+outfile.name)
    outfile.close()
    

               

if __name__ == "__main__":
  main()
