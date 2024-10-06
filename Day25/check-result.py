# Install with pip install firecrawl-py
from firecrawl import FirecrawlApp
from rich import print
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

crawl_status = app.check_crawl_status("你的 job id")
print(crawl_status)

# load data to file
with open('result.json', 'w') as f:
    json.dump(crawl_status, f, ensure_ascii=False)
