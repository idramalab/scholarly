import scholarly
import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) != 3:
	print("Usage: diff.py old.csv new.csv")
	exit()

file1 = str(sys.argv[1])
file2 = str(sys.argv[2])

columns = ['new_cites', 'cites', 'title',  'author', 'year', 'cites_per_year', 'eprint', 
'pages', 'publisher', 'url', 'id_citations', 'id_scholarcitedby', 'source', 'citedByUrl']


update = pd.DataFrame(columns=columns)

df1 = pd.read_csv(file1) 
df2 = pd.read_csv(file2) 

for i in range(df1.shape[0]):
	paper_id = df1.loc[i]['id_citations']
	paper_scholar = df1.loc[i]['id_scholarcitedby']
	cites1 = df1.loc[i]['cites']
	#print("Search " + paper_id + " " + df1.loc[i]['title'][0:20] + " with " + str(cites1) + " cites")
	cites2 = next(iter(df2.loc[df2['id_citations'] == paper_id]['cites']),'no match')
	if(cites2 == 'no match'):
		print("paper disappeared!")
		update = update.append(pd.Series([0, df1.loc[i]['cites'], df1.loc[i]['title'],  df1.loc[i]['author'], df1.loc[i]['year'], df1.loc[i]['cites_per_year'], df1.loc[i]['eprint'], df1.loc[i]['pages'], df1.loc[i]['publisher'], df1.loc[i]['url'], df1.loc[i]['id_citations'], df1.loc[i]['id_scholarcitedby'], df1.loc[i]['source'], df1.loc[i]['citedByUrl']], index=update.columns), ignore_index=True)
	elif(cites1 != cites2):
		print("Paper " + paper_scholar + " " + df1.loc[i]['title'][0:20] + " has gone from " + str(cites1) + " to " + str(cites2) + " cites")
		update = update.append(pd.Series([cites2, df1.loc[i]['cites'], df1.loc[i]['title'],  df1.loc[i]['author'], df1.loc[i]['year'], df1.loc[i]['cites_per_year'], df1.loc[i]['eprint'], df1.loc[i]['pages'], df1.loc[i]['publisher'], df1.loc[i]['url'], df1.loc[i]['id_citations'], df1.loc[i]['id_scholarcitedby'], df1.loc[i]['source'], df1.loc[i]['citedByUrl']], index=update.columns), ignore_index=True)

for i in range(df2.shape[0]):
	paper_id = df2.loc[i]['id_citations']
	paper_scholar = df2.loc[i]['id_scholarcitedby']
	cites2 = df2.loc[i]['cites']
	#print("Search " + paper_id + " " + df1.loc[i]['title'][0:20] + " with " + str(cites1) + " cites")
	cites1 = next(iter(df1.loc[df1['id_citations'] == paper_id]['cites']),'no match')
	if(cites1 == 'no match'):
		print("New paper!")
		update = update.append(pd.Series([df2.loc[i]['cites'], 0, df2.loc[i]['title'],  df2.loc[i]['author'], df2.loc[i]['year'], df2.loc[i]['cites_per_year'], df2.loc[i]['eprint'], df2.loc[i]['pages'], df2.loc[i]['publisher'], df2.loc[i]['url'], df2.loc[i]['id_citations'], df2.loc[i]['id_scholarcitedby'], df2.loc[i]['source'], df2.loc[i]['citedByUrl']], index=update.columns), ignore_index=True)

filename = "update.csv"
print("Done. Saving to file... " + filename)
update.to_csv(filename,index=False)


