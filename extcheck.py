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

        
def main():
    print 'Running parent script'
    call(["git", "commit","-a","-m", "autorun"])
    time.sleep(10)
    call(["git", "push"])
    time.sleep(10)
    
    
    
 

if __name__ == "__main__":
  main()
