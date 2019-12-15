import scholarly
import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) != 2:
	print("Usage: author.py \"author name\"")
	exit()

author_name = str(sys.argv[1])
print("Searching " + author_name + " on Google Scholar. This might take a while...")

search_query = scholarly.search_author(author_name)
author = next(search_query).fill()
print("Successfully retrieved profile.")

columns = ['name', 'id', 'link', 'affiliation', 'citedby', 'citedby5y', 'hindex', 'hindex5y', 'i10index', 'i10index5y', 
'cites_per_year', 'email', 'interests', 'url_picture']

profile = pd.DataFrame(columns=columns)

profile = profile.append(pd.Series([getattr(author,'name'), 
getattr(author,'id'),
"https://scholar.google.com/citations?hl=en&user=" + getattr(author,'id'),
getattr(author,'affiliation'),
getattr(author,'citedby'),
getattr(author,'citedby5y'),
getattr(author,'hindex'),
getattr(author,'hindex5y'),
getattr(author,'i10index'),
getattr(author,'i10index5y'),
getattr(author,'cites_per_year'),
getattr(author,'email'),
getattr(author,'interests',""),
getattr(author,'url_picture')
], index=profile.columns), ignore_index=True)

today = datetime.today().strftime('%Y%m%d')
filename = author_name.replace(" ", "") + "-profile_" + today + ".csv"
print("Saving to file... " + filename)
profile.to_csv(filename,index=False)
