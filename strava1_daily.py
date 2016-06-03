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
from subprocess import call
import strava1
import gitcommit
        
def main():
    print 'Running parent script'
    for i in range(365):
        strava1.main()
        gitcommit.main()
        time.sleep(78600)


if __name__ == "__main__":
  main()
