from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

'''
A script to scrape youtube links from a predefined website of choice.
'''

#funtion to extract youtube link from web pages
urls=deque()
urls.append('https://url_to_crawl')
def process_urls(urls_to_process):

	processed_urls = set()  # a set of urls that have already been crawled
	youtube_links = set()  # a set of extracted youtube links

	while len(urls_to_process) > 0:  # process urls one by one until we exhaust the queue

		f = open('YoutubeLinks.txt','a')

		url = urls_to_process.popleft()  # move next url from the queue to the set of processed urls
		processed_urls.add(url)
		parts = urlsplit(url)    # extract base url to resolve relative links
		base_url = "{0.scheme}://{0.netloc}".format(parts)
		path = url[:url.rfind('/')+1] if '/' in parts.path else url
		print("Processing %s" % url)
		try:
			response = requests.get(url)
		except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
		# ignore pages with errors
			continue
		new_youtube_link = set(re.findall(r"https://www.youtube.com/embed/[a-z,A-Z,0-9]+", response.text, re.I))   # extract all youtube_link addresses and add them into a set
		youtube_links.update(new_youtube_link)
		soup = BeautifulSoup(response.text)     # create a beautifulsoup for the html document

		if new_youtube_link:
			f.write('\n'.join(new_youtube_link))
			f.write('\n')
		f.close()

		#Extract more urls from current page after crawl :'<a> tags'
		for anchor in soup.find_all("a"):
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''  # extract link url from the anchor
			use_link = ''
			if link.startswith('base_url'):   # ensure link is part of current domain not cross-site 
				use_link = link

			if not use_link in urls_to_process and not use_link in processed_urls:   # add the new url to the queue if it was not enqueued nor processed yet
				urls_to_process.append(use_link)


	return

process_urls(urls)
