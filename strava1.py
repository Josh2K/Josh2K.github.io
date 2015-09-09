#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from bs4 import BeautifulSoup

from stravalib.client import Client
import csv
import time
import datetime

def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


def segment_details(num,segment,topguy,friend_colour_dict):

    id = num + 1
    segment_id = segment.id
    segment_name = segment.name.encode('utf-8')
    segment_name = re.sub(',', "", segment_name)
    url = 'http://www.strava.com/segments/'+str(segment_id)+'/compare/'

    start_latitude = segment.start_latitude
    start_longitude = segment.start_longitude
    end_latitude = segment.end_latitude
    end_longitude = segment.end_longitude

    tuple=(str(num),str(start_latitude),str(start_longitude),str(segment_name)+':  ['+str(topguy)+']',str(topguy),str(friend_colour_dict[topguy]),str(segment_name),str(segment_id),str(url))
    now = datetime.datetime.now()
    print str(now)+': ID: '+str(id)+'     Segment ID:  '+str(segment_id)+'   Owner:  '+str(topguy)
    return tuple
    

        
def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')

    segmentlist = []
    file = open('segments.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    badsegments = ['4571910','6707104','8002513','5216188','6570485']

    #get rid of badsegments
    for x in badsegments:
        if x in segmentlist:
            segmentlist.remove(x)
        
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    josh_friends = client.get_athlete_friends(5991862)
    for a in josh_friends:
        print("{} is Josh's friend.".format(a.firstname))
        
    #colors
    colours = ['575757','FFCDF3','FFEE33','FF9233','29D0D0','8126C0','814A19','1D6914','2A4BD7','AD2323','000000','88C6ED','82C341']
    
    segoutfile = open('segoutput.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    friend_colour_dict = {}
    friend_colour_dict['UNCLAIMED'] = '000000'
    friend_colour_dict['Patrick Santeusanio'] = 'AD2323'
    friend_colour_dict['Marc Devlin'] = '2A4BD7'
    friend_colour_dict['Mike Sants'] = '1D6914'
    friend_colour_dict['Josh Felker'] = '814A19'
    friend_colour_dict['Yibing Wen'] = '8126C0'
    friend_colour_dict['Arvind Ramanathan'] = '29D0D0'
    friend_colour_dict['Mario Born'] = 'FF9233'
    friend_colour_dict['Sasha Wloski'] = 'FFEE33'
    friend_colour_dict['Frank Oduro'] = 'FFCDF3'
    friend_colour_dict['Avalon Powell'] = '575757'
    friend_colour_dict['Eoin Craigie'] = '88C6ED'
    
    
    
    
    
    
    for num,j in enumerate(segmentlist):
        time.sleep(5)
        segment = client.get_segment(j)
                        
        try:
            leaderboard = client.get_segment_leaderboard(j,following=True)
            if not leaderboard:
                topguy = 'UNCLAIMED'
            else:
                topguy = leaderboard[0].athlete_name
            
            if not topguy in friend_colour_dict:
                friend_colour_dict[topguy] = colours.pop()
                
        
            for z in segment_details(num,segment,topguy,friend_colour_dict):
                segoutfile.write(str(z)+',')
            segoutfile.write('\n')
            
   
        except Exception:
            badoutfile = open('bad_segments.csv', 'a+')
            badoutfile.write(str(j)+',')
            badoutfile.close()
            pass
                          

if __name__ == "__main__":
  main()
