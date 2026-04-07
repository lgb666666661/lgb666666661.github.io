from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os
import sys

def log(msg):
    print(msg, flush=True)

log("=== main.py start ===")

log("Step 1: reading GOOGLE_SCHOLAR_ID from environment")
scholar_id = os.environ['GOOGLE_SCHOLAR_ID']
log(f"Step 2: GOOGLE_SCHOLAR_ID loaded: {scholar_id}")

log("Step 3: calling scholarly.search_author_id(...)")
author: dict = scholarly.search_author_id(scholar_id)
log("Step 4: scholarly.search_author_id(...) finished")

log("Step 5: calling scholarly.fill(..., sections=['basics', 'indices', 'counts', 'publications'])")
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
log("Step 6: scholarly.fill(...) finished")

log("Step 7: reading author name")
name = author['name']
log(f"Step 8: author name = {name}")

log("Step 9: setting updated time")
author['updated'] = str(datetime.now())

log("Step 10: converting publications to dict by author_pub_id")
author['publications'] = {v['author_pub_id']: v for v in author['publications']}
log("Step 11: publications conversion finished")

log("Step 12: printing author json")
print(json.dumps(author, indent=2), flush=True)

log("Step 13: creating results directory")
os.makedirs('results', exist_ok=True)

log("Step 14: writing results/gs_data.json")
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)
log("Step 15: wrote results/gs_data.json")

log("Step 16: preparing shields.io data")
shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}

log("Step 17: writing results/gs_data_shieldsio.json")
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
log("Step 18: wrote results/gs_data_shieldsio.json")

log("=== main.py done ===")
