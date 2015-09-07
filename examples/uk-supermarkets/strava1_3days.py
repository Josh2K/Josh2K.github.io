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
import strava1

        
def main():
    print 'Running parent script'
    for i in range(365):
        strava1.main()
        time.sleep(259200)
 

if __name__ == "__main__":
  main()
