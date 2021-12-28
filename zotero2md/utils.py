from collections import defaultdict
from typing import Dict, List

from pyzotero.zotero import Zotero


def group_annotations_by_parent_file(annotations: List[Dict]) -> defaultdict:
    annotations_by_parent = defaultdict(list)
    for annot in annotations:
        annotations_by_parent[annot["data"]["parentItem"]].append(annot)
    return annotations_by_parent


def sanitize_tag(tag: str):
    return tag.strip().replace(" ", "_")


def retrieve_all_annotations(zotero_client: Zotero):
    print("Retrieving ALL annotations from Zotero Database. \nIt may take some time...")
    return zotero_client.everything(zotero_client.items(itemType="annotation"))


def retrieve_all_notes(zotero_client: Zotero):
    print("Retrieving ALL notes from Zotero Database. \nIt may take some time...")
    return zotero_client.everything(zotero_client.items(itemType="note"))
