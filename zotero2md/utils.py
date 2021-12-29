from collections import defaultdict
from typing import Dict, List

from pyzotero.zotero import Zotero


def group_annotations_by_parent_file(annotations: List[Dict]) -> defaultdict:
    annotations_by_parent = defaultdict(list)
    for annot in annotations:
        annotations_by_parent[annot["data"]["parentItem"]].append(annot)
    return annotations_by_parent


def sanitize_tag(tag: str) -> str:
    """Clean tag by replacing empty spaces with underscore.

    Parameters
    ----------
    tag: str

    Returns
    -------
    str
        Cleaned tag

    Examples
    --------
    >>> sanitize_tag(" Machine Learning ")
    "Machine_Learning"

    """
    return tag.strip().replace(" ", "_")


def sanitize_filename(filename: str) -> str:
    """Clean filename
    Replace illegal (or problem-causing) characters with empty spaces, dashes or nothing.
    char_to_replace dictionary contains the mapping.

    Parameters
    ----------
    filename: str
        original filename

    Returns
    -------
    str
        Sanitized filename (without extension)

    Examples
    --------
    >>> sanitize_filename(" abc.pdf")
    "abc"
    >>> sanitize_filename("abc:def?ghi")
    "abc -- ghi"
    >>> sanitize_filename("abc.def")
    "abc def"

    """
    out_filename = filename.strip()
    char_to_replace = {".pdf": " ", ":": " -- ", "/": "-", "?": " ", ".": " "}
    for old, new in char_to_replace.items():
        out_filename = out_filename.replace(old, new)
    return out_filename


def retrieve_all_annotations(zotero_client: Zotero):
    print(
        "Retrieving ALL annotations from Zotero Database. \nIt may take some time...\n"
    )
    return zotero_client.everything(zotero_client.items(itemType="annotation"))


def retrieve_all_notes(zotero_client: Zotero):
    print("Retrieving ALL notes from Zotero Database. \nIt may take some time...\n")
    return zotero_client.everything(zotero_client.items(itemType="note"))
