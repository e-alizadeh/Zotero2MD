import json
from collections import defaultdict
from dotenv import load_dotenv
import os
from pyzotero.zotero import Zotero
# from dataclass import dataclass
from typing import Dict, List

from snakemd import Document

# Load environment variables
load_dotenv('secrets.env')

zot = Zotero(library_id=os.environ["LIBRARY_ID"], library_type="user", api_key=os.environ["API_KEY"])

all_items = zot.everything(zot.all_top())

all_annotations = zot.everything(zot.items(itemType="annotation"))
all_notes = zot.everything(zot.items(itemType="note"))

COLORS = dict(
    red="#ff6666",
    green="#5fb236",
    blue="#2ea8e5",
    yellow="#ffd400",
    purple="#a28ae5",
)
HEX_to_COLOR = {v: k for k, v in COLORS.items()}


with open('all_annotations.json', 'w') as f:
    json.dump(all_annotations, f)
#
with open('all_annotations.json', 'r') as f:
    data = json.load(f)

def group_annotations_by_parent_file(annotations: List[Dict]) -> defaultdict:
    annotations_by_parent = defaultdict(list)
    for annot in annotations:
        annotations_by_parent[annot["data"]["parentItem"]].append(annot)
    return annotations_by_parent


counts = {}
for item in all_items:
    item_type = item['data']['itemType']
    counts[item_type] = counts.get(item_type, 0) + 1



def format_highlight(highlight: Dict) -> str:
    data = highlight['data']
    # zotero_unique_id = f"(key={highlight['key']}, version={highlight['version']})"
    return (
        f"{data['annotationText']} "
        f"(Page {data['annotationPageLabel']})" 
        f"<!--(Highlighted on {data['dateAdded']})-->"
        # f"<!---->"
    )


def create_highlights_section(doc: Document, highlights: List) -> None:
    doc.add_header(level=1, text="Highlights")
    doc.add_unordered_list(
        format_highlight(h) for h in highlights
    )


def format_tags(tags: List[str], internal_link: bool = True) -> str:
    if internal_link:
        return " ".join([f"[[{tag}]]" for tag in tags])
    else:
        return " ".join([f"#{tag}" for tag in tags])

def create_metadata_section(doc: Document, metadata: Dict, is_tag_internal_link = True) -> None:
    doc.add_header(level=1, text="Metadata")
    authors = metadata.get('creators', None)

    output: List = []

    if len(authors) == 1:
        output.append(f"Author: {authors[0]}")
    elif 1 < len(authors) <= 5:
        output.append(f"Authors: {', '.join(authors)}")
    elif len(authors) > 5:
        output.append(f"Authors: {authors[0]} et al.")

    if metadata.get('date', None):
        output.append(f"Date: {metadata['date']}")
    
    tags = metadata.get('tags', None)

    if tags:
        output.append(format_tags(tags, is_tag_internal_link))



    doc.add_unordered_list(
        [
            
        ]
    )

d = group_annotations_by_parent_file(all_annotations)
item_key = "UIBHCUP6"
# item_key = 'N69RPVEF'
item_highlights = d[item_key]
item_details = zot.item(item_key)

def get_item_metadata(item_details: Dict) -> Dict:
    if "parentItem" in item_details['data']:
        top_parent_item = zot.item(item_details['data']['parentItem'])
        data = top_parent_item["data"]
        metadata = {
            "title": data["title"],
            "date": data["date"],
            "creators": [creator["firstName"] + " " + creator["lastName"] for creator in data["creators"]],
            "tags": data["tags"],
        }
    else:
        data = item_details['data']
        metadata = {
            "title": data["title"],
            "tags": data["tags"],
        }

    return metadata

metadata = get_item_metadata(item_details)

# def create_md_doc(highlights, notes, metadata, frontmatter) -> None:

doc = Document(metadata["title"])

# doc.add_element()
doc.add_header(level=1, text="Metadata")

create_highlights_section(doc, item_highlights)