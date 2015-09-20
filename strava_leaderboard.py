#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from bs4 import BeautifulSoup
import json
import requests

from stravalib.client import Client


import csv
import time
import datetime

def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def outputfile_exists():
    if os.path.exists('./distance.csv'):
        return True
    else:
        return False

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

def fetch_data(friend,now):
    time.sleep(6)
    friend_name = friend.firstname+' '+friend.lastname
    url = requests.get('http://www.strava.com/athletes/'+str(friend.id))
    soup = BeautifulSoup(url.content, "html.parser")
    tables = soup.findAll('table')
    tablerows = tables[0].findAll('tr')
    for row in tablerows:
        if row.find('th').text == 'Distance':
            friend_distance_raw = row.find('td').text
            friend_distance = cleanconvert(friend_distance_raw)
    print str(now)+'  :'+friend_name+' - '+str(friend_distance)
    tuple=(str(now),friend_name,friend_distance)
    return(tuple)

        
def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')
   
    

    now = datetime.datetime.now().strftime('%Y-%m-%d')
    
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()

    #print("{} - Hello, {}. I know your email is {}".format(now,athlete.firstname, athlete.email))

    josh_friends = client.get_athlete_friends(5991862)
    
    outputlist = []
    for friend in josh_friends:        
        outputlist.append(fetch_data(friend,now))
    outputlist.append(fetch_data(athlete,now))

   
    if outputfile_exists() == False:
        outfile = open('distance.csv', 'a+')
        outfile.write('datetime,name,distance'+'\n')
        outfile.close()
    outfile = open('distance.csv', 'a+')
    for s in outputlist:
        for z in s:
            outfile.write(str(z)+',')
        
        outfile.write('\n')
    print str(now)+'  :  ACTION:    new data added to '+outfile.name
    outfile.close()
    
           

if __name__ == "__main__":
  main()
