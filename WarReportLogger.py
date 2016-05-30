#!/usr/bin/python

import pandas as pd
from datetime import datetime
import numpy as np
from collections import defaultdict
import operator


df1 = pd.read_csv('segoutput.csv',index_col=False)
df1 = df1.set_index(['segment_id'])
df2 = pd.read_csv('segoutput_ref.csv',index_col=False)
df2 = df2.set_index(['segment_id'])
df2

def main_logger(df1,df2):

	#don't understand the following block of code:
	ne = (df2 != df1).any(1)
	ne_stacked = (df2 != df1).stack()
	changed = ne_stacked[ne_stacked]
	difference_locations = np.where(df2 != df1)
	changed_from = df2.values[difference_locations]
	changed_to = df1.values[difference_locations]
	changed_df = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)

	changed_df2 = changed_df.unstack() 
	# its making some sort of multi-index array but I can't figure out how to slice or work with the data.  Unstack atleast gets
	#it back into a form I can work with but this seems very inefficient, need to figure out how to work with multi-index df

	changed_from2 = changed_df2['from']['type']
	changed_to2 = changed_df2['to']['type']

	df_changed_from = pd.DataFrame(changed_from2)
	df_changed_from = df_changed_from[df_changed_from.type.notnull()]

	df_changed_to = pd.DataFrame(changed_to2)
	df_changed_to = df_changed_to[df_changed_to.type.notnull()]


	war_report_dict = {}
	for x in df_changed_to['type'].unique():
		#print 'this is x: ',x
		personcount = defaultdict(int)
		
		for y in df_changed_to[df_changed_to['type'] == x].index:
			
			#don't get why the output here is a numpy array:
			beatperson_array = df_changed_from[df_changed_from.index == y].values[0]
			
			#converting to string:
			beatperson_string = str(beatperson_array[0])
			
			personcount[beatperson_string] += 1
			  
		war_report_dict[x] = personcount
				   

	for warlord in war_report_dict:
		for victim in sorted(war_report_dict[warlord].items(), key=operator.itemgetter(1), reverse=True):
			if victim[0] == 'UNCLAIMED':
				print warlord,'claimed',victim[1],'unowned territories'
			else:
				print warlord,'conquered',victim[1],'territories from',victim[0]
			
        

		
if __name__ == "__main__":
  main()

        





