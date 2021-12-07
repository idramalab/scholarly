from scholarly import scholarly
import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) != 2:
	print("Usage: author.py \"author name\"")
	exit()

author_name = str(sys.argv[1])
print("Searching " + author_name + " on Google Scholar. This might take a while...")

search_query = scholarly.search_author(author_name)
first_author_result = next(search_query)
#scholarly.pprint(first_author_result)

author = scholarly.fill(first_author_result)
#scholarly.pprint(author)
print("Successfully retrieved profile.")

columns = ['name', 'scholar_id', 'link', 'affiliation', 'citedby', 'citedby5y', 'hindex', 'hindex5y', 'i10index', 'i10index5y', 
'cites_per_year', 'interests']

profile = pd.DataFrame(columns=columns)

print(author['name'])

profile = profile.append(pd.Series([author['name'], 
author['scholar_id'],
"https://scholar.google.com/citations?hl=en&user=" + author['scholar_id'],
author['affiliation'],
author['citedby'],
author['citedby5y'],
author['hindex'],
author['hindex5y'],
author['i10index'],
author['i10index5y'],
author['cites_per_year'],
author['interests']
], index=profile.columns), ignore_index=True)

today = datetime.today().strftime('%Y%m%d')
filename = author_name.replace(" ", "") + "-profile_" + today + ".csv"
print("Saving to file... " + filename)
profile.to_csv(filename,index=False)
