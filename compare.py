#!/usr/bin/python


import sys
import pandas as pd
from WarReportLogger import main_logger


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')

    df1 = pd.read_csv('segoutput_old.csv', index_col=False)
    df1 = df1.set_index(['segment_id'])

    df2 = pd.read_csv('segoutput.csv', index_col=False)
    df2 = df2.set_index(['segment_id'])
    try:
        main_logger(df2, df1)
        # strava1 main_logger (warlog creation)
        res = requests.get("https://nosnch.in/ae58837141")
    except Exception as e:
        print 'Error: ' + str(e)
        pass

    # strava1_segment main
    res = requests.get("https://nosnch.in/26ba53ff3d")


if __name__ == "__main__":
    main()
