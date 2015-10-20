#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import csv
from collections import defaultdict
from stravalib.client import Client
import csv
import time
import datetime
import json
import operator

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}

def main():
    reload(sys)  
    sys.setdefaultencoding('utf8')

   
        
    client = Client(access_token='76824abf6abf903eb3d8b0bde83625135c0be0ec')
    athlete = client.get_athlete()
    print("Hello, {}. I know your email is {}".format(athlete.firstname, athlete.email))
    josh_friends = client.get_athlete_friends(5991862)
    print "Starting...."        
    leaderboard = client.get_segment_leaderboard(2658830,following=True)
    print leaderboard[0].athlete_name

    friend_colour_dict = {}
    friend_colour_file = open('friend_colour.csv')
    colourreader = UnicodeDictReader(friend_colour_file)
    for line in colourreader:
        friend_colour_dict[line["name"]] = line["colour"]

    for x in friend_colour_dict:
        print str(x).encode("utf8")
    
            
              

if __name__ == "__main__":
  main()
