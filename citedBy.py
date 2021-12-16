from scholarly import scholarly
import pandas as pd
import sys
from datetime import datetime
import time
import random
from scholarly import ProxyGenerator


if len(sys.argv) != 2:
	print("Usage: citedBy.py \"Paper Title\"")
	exit()

pg = ProxyGenerator()
success = pg.ScraperAPI("2f390977f8a7b3df40d092926587b667")
scholarly.use_proxy(pg)
print("Now using Proxy")


paper_title = str(sys.argv[1])
print("Searching " + paper_title + " on Google Scholar. This might take a while...")

search_query = scholarly.search_pubs(paper_title)
first_result = next(search_query)
#scholarly.pprint(first_result)

seed = scholarly.fill(first_result)
#scholarly.pprint(paper)
print("Successfully retrieved paper\n\n")


columns = ['cites', 'title', 'author', 'year', 'pub_url', 'publisher']
papers = pd.DataFrame(columns=columns)

pubs = []
#citations = [citation['bib']['title'] for citation in scholarly.citedby(paper)]


for cit in scholarly.citedby(seed):
	print(cit['bib']['title'])
	#pub = scholarly.fill(cit)
	#print("Filled")
	pubs.append(cit)
	#s = random.uniform(5,15)
	#print("Sleeping for " + s + " seconds")
	#time.sleep(random.uniform(5,15))
#	print(pub['bib'].get('title'))

print("Done with citedby retrieval. Now saving shit.")

for i in range(len(pubs)):
	#print("Processing pub " + str(i+1) + "/" + str(len(pubs)))
	pub = pubs[i]
	papers = papers.append(pd.Series([
	pub.get('num_citations'),
	pub['bib'].get('title'),
	pub['bib'].get('author'),
	pub['bib'].get('pub_year'),
	pub.get('pub_url'),
	pub['bib'].get('publisher')
	], index=papers.columns), ignore_index=True)

today = datetime.today().strftime('%Y%m%d')
filename = paper_title.replace(" ", "") + "_complete_" + today + ".csv"
print("Done. Saving to file... " + filename)
papers.to_csv(filename,index=False)
