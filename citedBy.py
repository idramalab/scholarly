from scholarly import scholarly
import pandas as pd
import sys
from datetime import datetime

if len(sys.argv) != 2:
	print("Usage: citedBy.py \"Paper Title\"")
	exit()

paper_title = str(sys.argv[1])
print("Searching " + paper_title + " on Google Scholar. This might take a while...")

search_query = scholarly.search_pubs(paper_title)
first_result = next(search_query)
#scholarly.pprint(first_result)

seed = scholarly.fill(first_result)
#scholarly.pprint(paper)
print("Successfully retrieved paper\n\n")


columns = ['cites', 'title', 'author', 'year', 'cites_per_year', 'pub_url', 'publisher', 'cites_id', 'citedby_url']
papers = pd.DataFrame(columns=columns)

pubs = []
#citations = [citation['bib']['title'] for citation in scholarly.citedby(paper)]
for cit in scholarly.citedby(seed):
	pub = scholarly.fill(cit)
	pubs.append(pub)
#	print(pub['bib'].get('title'))

for i in range(len(pubs)):
	print("Processing pub " + str(i+1) + "/" + str(len(pubs)))
	pub = pubs[i]
	papers = papers.append(pd.Series([
	pub.get('num_citations'),
	pub['bib'].get('title'),
	pub['bib'].get('author'),
	pub['bib'].get('pub_year'),
	pub.get('cites_per_year'),
	pub.get('pub_url'),
	pub['bib'].get('publisher'),
	pub.get('cites_id'),
	pub.get('citedby_url')
	], index=papers.columns), ignore_index=True)

today = datetime.today().strftime('%Y%m%d')
filename = paper_title.replace(" ", "") + "_complete_" + today + ".csv"
print("Done. Saving to file... " + filename)
profile.to_csv(filename,index=False)
