#!/usr/bin/python

import sys
import re
import csv
from stravalib.client import Client
from retrying import retry
import time
import datetime
import json
import pandas as pd
import requests
from WarReportLogger import main_logger

def segment_details(num,segment,topguy,friend_df):

    id = num + 1
    segment_id = segment.id
    segment_name = segment.name
    segment_name = re.sub(',', "", segment_name)
    url = 'http://www.strava.com/segments/'+str(segment_id)+'/compare/'

    start_latitude = segment.start_latitude
    start_longitude = segment.start_longitude
    end_latitude = segment.end_latitude
    end_longitude = segment.end_longitude
    colour = friend_df.loc[friend_df['shortname'] == topguy,'colour'].values[0]
    topguy_fullname = friend_df.loc[friend_df['shortname'] == topguy,'name'].values[0]

    tuple=(str(num),str(start_latitude),str(start_longitude),str(segment_name)+':  ['+str(topguy_fullname)+']',str(topguy_fullname),str(colour),str(segment_name),str(segment_id),str(url))
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print('\r'+str(now)+': ID: '+str(id)+'     Segment ID:  '+str(segment_id)+'   Owner:  '+str(topguy_fullname),)
    return tuple
    
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_segment(client,j):
    return client.get_segment(j)

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_leaderboard(client,j,club):
    return client.get_segment_leaderboard(j,club_id=club)

 
def main():
    #reload(sys)  
    #sys.setdefaultencoding('utf8')
    
    df1 = pd.read_csv('segoutput.csv',index_col=False)
    df1 = df1.set_index(['segment_id'])
    
    segmentlist = []
    file = open('segments.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    
    club = 202883
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
            
    segoutfile = open('segoutput.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    
    friend_df = pd.read_csv('friend_colour_new.csv',index_col=False)
        
    friend_count_dict = {} 
           
    
    for num,j in enumerate(segmentlist):
        time.sleep(3)
        segment = retry_get_segment(client,j)
                                
        try:
            leaderboard = retry_get_leaderboard(client,j,club)
            if not leaderboard:
                topguy = 'UNCLAIMED'
                topguy_id = 0
                 
            else:
                topguy = leaderboard[0].athlete_name

                #topguy_id = leaderboard[0].athlete_id
                           
                            
            if not topguy in friend_df['shortname'].values:
                new_friend = {'name': topguy, 'id':'xxx', 'colour':'646464','shortname': topguy}
                friend_df = friend_df.append(new_friend, ignore_index=True)
              
                       
            if topguy in friend_count_dict:
                friend_count_dict[topguy] += 1
            else:
                friend_count_dict[topguy] = 1

                      
            
            for z in segment_details(num,segment,topguy,friend_df):
                segoutfile.write(str(z)+',')
            segoutfile.write('\n')            
            
    
        except Exception:
            badoutfile = open('bad_segments.csv', 'a+')
            badoutfile.write(str(j)+','+'\n')
            badoutfile.close()
            pass

    
    
    segoutfile.close()
    friend_df.to_csv('friend_colour_new.csv', index=False)
    
   
    #segment count output
    segcountoutfile = open('segmentcount.csv', 'w')
    segcountoutfile.write('name,colour,count'+'\n')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            print(str(x)+': '+str(friend_count_dict[x]))
            segcountoutfile.write(str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    segcountoutfile.write('\n')
    segcountoutfile.close()
    

    #segment count over time output
    segcountovertimefile = open('segmentcountovertime.csv', 'a+')
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            segcountovertimefile.write(str(nowdate)+','+str(friend_df.loc[friend_df['shortname'] == x,'name'].values[0])+','+str(friend_df.loc[friend_df['shortname'] == x,'colour'].values[0])+','+str(friend_count_dict[x])+'\n')
    segcountovertimefile.close()
    
    time.sleep(5)
    
    #read newly created segoutput.csv (df2) and compare it to original (df1):
    df2 = pd.read_csv('segoutput.csv',index_col=False)
    df2 = df2.set_index(['segment_id'])  
    try:
        main_logger(df2,df1)
    except Exception as e:
        print('Error: '+str(e))
        pass
    
                     

if __name__ == "__main__":
  main()
