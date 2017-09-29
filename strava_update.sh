#!/bin/bash
cd ~/Josh2K.github.io/
git fetch origin
git reset --hard origin/master
python strava_leaderboard.py >> strava_leaderboard_py_log.txt 2>&1
python strava_segments.py >> strava_segments_py_log.txt 2>&1
python strava_plots.py >> strava_plots.py_log_txt 2>&1
git add .
git commit -a -m 'cron attempt'
git push

