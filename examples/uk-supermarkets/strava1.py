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
    print 'ID: '+str(id)+'      Segment ID:  '+str(segment_id)+'    Owner:  '+str(topguy)
    return tuple
    

        
def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')

    segmentlist = []
    file = open('segments.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    badsegments = ['4571910','6707104']

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
    colours = ['575757','FFCDF3','FFEE33','FF9233','29D0D0','8126C0','814A19','1D6914','2A4BD7','AD2323','000000']

    #old colours
    #colours = ['DC143C','9932CC','0000FF','00CED1','00CD66','FFD700','00FF00','FFCC66','FFA500','FA8072','7171C6','1D6914','2A4BD7','AD2323','000000']
    
    
    
    segoutfile = open('segoutput.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    friend_colour_dict = {}
    

    for num,j in enumerate(segmentlist):
        time.sleep(6)
        segment = client.get_segment(j)
        
                
        
        #print segment.name
        
        leaderboard = client.get_segment_leaderboard(j,following=True) 
        
        if not leaderboard:
            topguy = 'UNCLAIMED'
        else:
            topguy = leaderboard[0].athlete_name
            
        if not topguy in friend_colour_dict:
            friend_colour_dict[topguy] = colours.pop()
                
        #segoutputlist.append(segment_details(num,segment,topguy,friend_colour_dict))

        for z in segment_details(num,segment,topguy,friend_colour_dict):
            segoutfile.write(str(z)+',')
        segoutfile.write('\n')
        
        

if __name__ == "__main__":
  main()
