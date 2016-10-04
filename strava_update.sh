#!/bin/bash
cd ~/Josh2K.github.iot/
python strava_leaderboard.py >> strava_leaderboard_py_log.txt 2>&1
python strava1.py >> strava1_py_log.txt 2>&1
git add .
git commit -a -m 'cron attempt'
git push

