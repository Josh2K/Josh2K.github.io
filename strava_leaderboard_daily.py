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
import csv
import time
import datetime
import strava_leaderboard

        
def main():
    print 'Running parent script'
    for i in range(365):
        strava_leaderboard.main()
        time.sleep(86400)
 

if __name__ == "__main__":
  main()
