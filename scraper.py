from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

#funtion to extract email addresses from web pages
urls=deque()
urls.append('https://www.examsolutions.net/tutorials/resultant-forces-two-forces-angle/?level=A-Level&board=AQA&module=Mechanics%20A-Level&topic=1632')
def process_urls(urls_to_process):

	processed_urls = set()  # a set of urls that have already been crawled
	emails = set()  # a set of extracted emails

	while len(urls_to_process) > 0:  # process urls one by one until we exhaust the queue

		f = open('Rainmails.txt','a')

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
		new_emails = set(re.findall(r"https://www.youtube.com/embed/[a-z,A-Z,0-9]+", response.text, re.I))   # extract all email addresses and add them into a set
		emails.update(new_emails)
		soup = BeautifulSoup(response.text)     # create a beutiful soup for the html document

		if new_emails:
			f.write('\n'.join(new_emails))
			f.write('\n')
		f.close()


		for anchor in soup.find_all("a"):
			link = anchor.attrs["href"] if "href" in anchor.attrs else ''  # extract link url from the anchor
			use_link = ''
			if link.startswith('https://www.examsolutions.net/'):   # resolve relative links
				use_link = link

			if not use_link in urls_to_process and not use_link in processed_urls:   # add the new url to the queue if it was not enqueued nor processed yet
				urls_to_process.append(use_link)

		
	# f = open('Rainmails.txt','w')    #indicate name of output file to write emails
	#sys.stdout = f
	#path= '/home/Desktop'  #for linux
	# f.write(repr(emails))

	return

process_urls(urls)