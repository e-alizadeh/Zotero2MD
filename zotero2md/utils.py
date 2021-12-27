from collections import defaultdict
from typing import Dict, List

from pyzotero.zotero import Zotero

from zotero2md import zotero_client


def group_annotations_by_parent_file(annotations: List[Dict]) -> defaultdict:
    annotations_by_parent = defaultdict(list)
    for annot in annotations:
        annotations_by_parent[annot["data"]["parentItem"]].append(annot)
    return annotations_by_parent


def sanitize_tag(tag: str):
    return tag.strip().replace(" ", "_")


def retrieve_all_annotations(zot: Zotero):
    return zot.everything(zotero_client.items(itemType="annotation"))


def retrieve_all_notes(zot: Zotero):
    return zot.everything(zotero_client.items(itemType="note"))
