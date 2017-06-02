#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from collections import defaultdict
from stravalib.client import Client
from retrying import retry
import csv
import time
import datetime
import json
import operator
import pandas as pd
import requests
from WarReportLogger import main_logger


def trim_count_overtime():
    friend_colour_dict = {}
    friend_colour_file = open('friend_colour.csv')
    colourreader = csv.DictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]
    del friend_colour_dict['UNCLAIMED']
    friendnames = []
    for x in friend_colour_dict:
        friendnames.append(x)

    date_dict = defaultdict(list)
    data_dict = defaultdict(list)
    with open('segmentcountovertime.csv', 'r') as csvinput:
        with open('trimmed_segmentcountovertime.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)
        
            row1 = next(reader)
            writer.writerow(row1)
            for x in reader:
                date_dict[x[0]].append(x[1])
                a = [x[1],x[3]]
                data_dict[x[0]].append(a)
            
            for x in friendnames:
                for y in date_dict.keys():
                    if x not in date_dict[y]:
                        data_dict[y].append([x,'0'])
            
            for x in sorted(data_dict.keys()):
                for y in data_dict[x]:
                    linelist = [str(x),str(y[0]),str(y[1])]
                    writer.writerow(linelist)
    return

def json_convert_trim_count_overtime():
    infile = open('trimmed_segmentcountovertime.csv')
    reader = csv.reader(infile)
    d_list = defaultdict(list)
    dict = {}
    row1 = next(reader)

    for x in reader:
        distance = float(x[2])
        d=x[0]
        p='%Y-%m-%d'
        epoch = int(time.mktime(time.strptime(d,p)) * 1000) 
        tuplist = [epoch,distance]
        name = x[1]
        d_list[name].append(tuplist)

    friend_colour_dict = {}
    friend_colour_file = open('friend_colour.csv')
    colourreader = csv.DictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]

    outfile = open('trimmed_segmentcountovertime.json', 'w')
    outfile.write('['+'\n')
    outfile.close()

    trimmed_d_list = {}
    for name,tuples in d_list.items():
        if name in friend_colour_dict:
            trimmed_d_list[name] = tuples

    for name,tuples in trimmed_d_list.items()[:-1]:
        if name in friend_colour_dict:
            singlenamedic = {}
            singlenamedic["key"] = name
            singlenamedic["values"] = tuples
            singlenamedic["color"] = '#'+str(friend_colour_dict[name])
            with open('trimmed_segmentcountovertime.json', 'a+') as outfile:
                json.dump(singlenamedic, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
                outfile.write(','+ '\n')

    for name,tuples in trimmed_d_list.items()[-1:]:
        if name in friend_colour_dict:
            singlenamedic = {}
            singlenamedic["key"] = name
            singlenamedic["values"] = tuples
            singlenamedic["color"] = '#'+str(friend_colour_dict[name])
            with open('trimmed_segmentcountovertime.json', 'a+') as outfile:
                json.dump(singlenamedic, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
                outfile.write('\n')

    outfile = open('trimmed_segmentcountovertime.json', 'a+')
    outfile.write('\n'+']')
    outfile.close()
    return

def json_convert_segmentcount():
    friend_colour_dict = {}
    friend_count_dict = {}

    friend_count_file = open('segmentcount.csv')
    countreader = csv.DictReader(friend_count_file)
    for line in countreader:
        friend_count_dict[line["name"]] = int(line["count"])
        friend_colour_dict[line["name"]] = '#'+line["colour"]


    listofdicts =[]
    for name,count in sorted(friend_count_dict.items(), key=operator.itemgetter(1), reverse=True):
        newdict = {}
        newdict['label'] = name
        newdict['value'] = friend_count_dict[name]
        newdict['color'] = friend_colour_dict[name]  
        listofdicts.append(newdict)
           
    outfile = open('segmentcount.json', 'w')
    outfile.write('['+'\n')
    outfile.close()

    singlenamedic = {}
    singlenamedic["key"] = 'Segment Count'
    singlenamedic["values"] = listofdicts
    with open('segmentcount.json', 'a+') as outfile:
        json.dump(singlenamedic, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write('\n')

    outfile = open('segmentcount.json', 'a+')
    outfile.write('\n'+']')
    outfile.close()
    return

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
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    print '\r'+str(now)+': ID: '+str(id)+'     Segment ID:  '+str(segment_id)+'   Owner:  '+str(topguy),
    return tuple
    
@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_segment(client,j):
    return client.get_segment(j)

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=30000)
def retry_get_leaderboard(client,j,club):
    return client.get_segment_leaderboard(j,club_id=club)

 
def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')
    
    df1 = pd.read_csv('segoutput.csv',index_col=False)
    df1 = df1.set_index(['segment_id'])
    
    segmentlist = []
    file = open('segments.csv')
    reader = csv.DictReader(file)
    for line in reader:
        segmentlist.append(line["Segment Id"])

    #get rid of badsegments
    badsegments = []
    badinfile = open('bad_segments.csv')
    badreader = csv.DictReader(badinfile)
    for line in badreader:
        badsegments.append(line["Segment Id"])
    print 'Bad Segments: '+str(badsegments)
    
    for x in badsegments:
        if x in segmentlist:
            segmentlist.remove(x)
        
    club = 202883
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    josh_friends = client.get_athlete_friends(5991862)
    print "Starting...."        
    #colors
    colours = ['575757','FFCDF3','FFEE33','FF9233','29D0D0','8126C0','814A19','1D6914','2A4BD7','AD2323','000000','88C6ED','C7258E']
    
    segoutfile = open('segoutput.csv', 'w')
    segoutfile.write('id,latitude,longitude,name,type,color,segment_name,segment_id,url'+'\n')
    segoutputlist = []

    friend_colour_dict = {}
    friend_colour_file = open('friend_colour.csv')
    colourreader = csv.DictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]

    friend_count_dict = {}
           
    
    for num,j in enumerate(segmentlist):
        time.sleep(3)
        segment = retry_get_segment(client,j)
                        
        try:
            leaderboard = retry_get_leaderboard(client,j,club)
            if not leaderboard:
                topguy = 'UNCLAIMED'
            else:
                topguy = leaderboard[0].athlete_name
                            
            if not topguy in friend_colour_dict:
                friend_colour_dict[topguy] = colours.pop()
                print str(topguy)+' not in friend_colour_dict, popping colour: '+ str(friend_colour_dict[topguy])

            if topguy in friend_count_dict:
                friend_count_dict[topguy] += 1
            else:
                friend_count_dict[topguy] = 1

                      
            
            for z in segment_details(num,segment,topguy,friend_colour_dict):
                segoutfile.write(str(z)+',')
            segoutfile.write('\n')
            
   
        except Exception:
            #badoutfile = open('bad_segments.csv', 'a+')
            #badoutfile.write(str(j)+','+'\n')
            #badoutfile.close()
            pass

    
    
    segoutfile.close()
    
    #segment count output
    segcountoutfile = open('segmentcount.csv', 'w')
    segcountoutfile.write('name,colour,count'+'\n')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            print str(x)+': '+str(friend_count_dict[x])
            segcountoutfile.write(str(x)+','+str(friend_colour_dict[x])+','+str(friend_count_dict[x])+'\n')
    segcountoutfile.write('\n')
    segcountoutfile.close()
    json_convert_segmentcount()
    


    #segment count over time output
    segcountovertimefile = open('segmentcountovertime.csv', 'a+')
    nowdate = datetime.datetime.now().strftime('%Y-%m-%d')
    for x in friend_count_dict:
        if x != 'UNCLAIMED':
            segcountovertimefile.write(str(nowdate)+','+str(x)+','+str(friend_colour_dict[x])+','+str(friend_count_dict[x])+'\n')
    segcountovertimefile.close()
    trim_count_overtime()
    json_convert_trim_count_overtime()

    time.sleep(5)
    #read newly created segoutput.csv (df2) and compare it to original (df1):
    df2 = pd.read_csv('segoutput.csv',index_col=False)
    df2 = df2.set_index(['segment_id'])  
    try:
        main_logger(df2,df1)
        #strava1 main_logger (warlog creation)
        res = requests.get("https://nosnch.in/ae58837141")
    except Exception as e:
        print 'Error: '+str(e)
        pass

    # strava1_segment main
    res = requests.get("https://nosnch.in/26ba53ff3d")
    
    
    
              

if __name__ == "__main__":
  main()
