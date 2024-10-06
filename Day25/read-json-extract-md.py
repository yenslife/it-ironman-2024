import json
from rich import print
import os

with open('result.json', 'r') as f:
    data = json.load(f)

print(len(data['data']))


# mkdir data
os.makedirs('data', exist_ok=True)
counter = 0
for item in data['data']:
    if item is None:
        continue
    try:
        title = item['metadata']['title']
    except Exception as e:
        print(e)    
        print(item)
        counter += 1
        title = f'{counter}.md'
    content = item['content']
    with open(f'data/{title}.md', 'w', encoding='utf-8') as f:
        f.write(content)
