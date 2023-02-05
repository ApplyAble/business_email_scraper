import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime
import re
import os

# load the API_KEY from the .env file
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')

NUM_RESULTS = 10  # 100 is the max
CONCURRENT_REQUESTS = 2  # 10 is the max

# take the queries from a csv file
def get_queries(filename):
    with open(filename, 'r') as f:
        queries = f.readlines()
    return [query.split(",")[0].strip() for query in queries]


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url,
               'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def create_google_url(query, site=''):
    google_dict = {'q': query, 'num': NUM_RESULTS, }
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
        return 'http://www.google.com/search?' + urlencode(google_dict)
    return 'http://www.google.com/search?' + urlencode(google_dict)


# read a line and scan for emails and return them
# return "" if no emails found
def get_emails(line):
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', line)
    if emails:
        return emails
    return ""

class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS_PER_DOMAIN': CONCURRENT_REQUESTS}

    def start_requests(self):
        queries = get_queries('businesses.csv')
        for query in queries:
            url = create_google_url(query)
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})

    def parse(self, response):
        di = json.loads(response.text)

        # get the query
        query = di['search_information']['query_displayed']

        pos = response.meta['pos']
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for result in di['organic_results']:
            title = result['title']
            snippet = result['snippet']
            email = get_emails(snippet)
            link = result['link']
            item = {'query': query, 'title': title, 'snippet': snippet,
                    'link': link, 'position': pos, 'date': dt, 'email': email}
            pos += 1
            yield item
        next_page = di['pagination']['nextPageUrl']
        if next_page:
            yield scrapy.Request(get_url(next_page), callback=self.parse, meta={'pos': pos})
