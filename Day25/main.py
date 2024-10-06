# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp
from rich import print
from dotenv import load_dotenv
import os

load_dotenv()

app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

crawl_result = app.crawl_url('https://housing-osa.ncku.edu.tw', params={
'limit': 10,
'scrapeOptions': {
	'formats': [ 'markdown' ],
  }
}, wait_until_done=False)

print(crawl_result)
job_id = crawl_result['jobId']
status = app.check_crawl_status(job_id)
print(status)
