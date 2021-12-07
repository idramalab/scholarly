from scholarly import scholarly
import pandas as pd
import sys
from datetime import datetime


if len(sys.argv) != 2:
	print("Usage: profile.py \"author name\"")
	exit()

author_name = str(sys.argv[1])
print("Searching " + author_name + " on Google Scholar. This might take a while...")

search_query = scholarly.search_author(author_name)
first_author_result = next(search_query)
#scholarly.pprint(first_author_result)

author = scholarly.fill(first_author_result)
#scholarly.pprint(author)
print("Successfully retrieved profile.")

columns = ['cites', 'title', 'author', 'year', 'cites_per_year', 'pub_url', 'publisher', 'cites_id', 'citedby_url']

profile = pd.DataFrame(columns=columns)

num_pubs = len(author['publications'])

print(author_name + " has " + str(num_pubs) + " papers on Scholar.")

#print(author['publications'][0]['bib'].get('title'))

for i in range(len(author['publications'])):
	print("Processing pub " + str(i+1) + "/" + str(num_pubs))
	tmp = author['publications'][i]
	pub = scholarly.fill(tmp)
	profile = profile.append(pd.Series([
	pub.get('num_citations'),
	pub['bib'].get('title'),
	pub['bib'].get('author'),
	pub['bib'].get('pub_year'),
	pub.get('cites_per_year'),
	pub.get('pub_url'),
	pub['bib'].get('publisher'),
	pub.get('cites_id'),
	pub.get('citedby_url')
	], index=profile.columns), ignore_index=True)
	print(profile.loc[i])

today = datetime.today().strftime('%Y%m%d')
filename = author_name.replace(" ", "") + "_" + today + ".csv"
print("Done. Saving to file... " + filename)
profile.to_csv(filename,index=False)
