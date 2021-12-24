import json
from collections import defaultdict
from dotenv import load_dotenv
import os
from pyzotero.zotero import Zotero

# Load environment variables
load_dotenv('secrets.env')

zot = Zotero(library_id=os.environ["LIBRARY_ID"], library_type="user", api_key=os.environ["API_KEY"])

all_items = zot.everything(zot.all_top())

all_annotations = zot.everything(zot.items(itemType="annotation"))


COLORS = dict(
    red="#ff6666",
    green="#5fb236",
    blue="#2ea8e5",
    yellow="#ffd400",
    purple="#a28ae5",
)
HEX_to_COLOR = {v: k for k, v in COLORS.items()}


with open('all_items.json', 'w') as f:
    json.dump(all_items, f)

#
# with open('all_annotations.json', 'r') as f:
#     data = json.load(f)

annot_by_parent = defaultdict(list)

for annot in all_annotations:
    parent_id = annot["data"]["parentItem"]
    annot_by_parent[parent_id].append(annot)

counts = {}
for item in all_items:
    item_type = item['data']['itemType']
    counts[item_type] = counts.get(item_type, 0) + 1

