#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
from bs4 import BeautifulSoup
import json
import requests
from stravalib.client import Client
from collections import defaultdict
import csv
import time
import datetime


def json_convert():
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
  
        
def main():
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
    json_convert()

if __name__ == "__main__":
  main()
