## needed files:

	strava_leaderboard.py
		input:
			friend_colour_new.csv

		output:
			distance.csv

	strava_segments.py
		input:
			friend_colour_new.csv
			segments.csv
			segoutput.csv

		output:
			segoutput.csv
			bad_segments.csv
			segmentcount.csv
			segmentcountovertime.csv

	segment_plots.py
		input:
			segmentcountovertime.csv
			segmentcount.csv

	WarReportLogger.py
		input:
			segoutput.csv
			segoutput_ref.csv
			warlog.csv


	stava_update.sh

