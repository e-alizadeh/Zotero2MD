import json
import os

# from dataclass import dataclass
from typing import Dict, List

from dotenv import load_dotenv
from pyzotero.zotero import Zotero
from snakemd import Document

# Load environment variables
from zt2md.utils import group_annotations_by_parent_file

load_dotenv("./secrets.env")

zot = Zotero(
    library_id=os.environ["LIBRARY_ID"],
    library_type="user",
    api_key=os.environ["ZOTERO_API_KEY"],
)
all_annotations = zot.everything(zot.items(itemType="annotation"))
# all_notes = zot.everything(zot.items(itemType="note"))
# all_items = zot.everything(zot.all_top())

with open("../all_annotations.json", "w") as f:
    json.dump(all_annotations, f)
#
with open("../all_annotations.json", "r") as f:
    all_annotations = json.load(f)

COLORS = dict(
    red="#ff6666",
    green="#5fb236",
    blue="#2ea8e5",
    yellow="#ffd400",
    purple="#a28ae5",
)
HEX_to_COLOR = {v: k for k, v in COLORS.items()}


class ZoteroItemBase:
    def __init__(self):
        self.zotero: Zotero = zot

    def get_item_metadata(self, item_details: Dict) -> Dict:
        if "parentItem" in item_details["data"]:
            top_parent_item = self.zotero.item(item_details["data"]["parentItem"])
            data = top_parent_item["data"]
            metadata = {
                "title": data["title"],
                "date": data["date"],
                "creators": [
                    creator["firstName"] + " " + creator["lastName"]
                    for creator in data["creators"]
                ],
                "tags": data["tags"],
            }
        else:
            data = item_details["data"]
            metadata = {
                "title": data["title"],
                "tags": data["tags"],
            }

        return metadata

    @staticmethod
    def format_tags(tags: List[str], internal_link: bool = True) -> str:
        if internal_link:
            return " ".join([f"[[{tag}]]" for tag in tags])
        else:
            return " ".join([f"#{tag}" for tag in tags])

    def format_metadata(self, metadata: Dict, is_tag_internal_link=True) -> List:
        output: List = []
        authors = metadata.get("creators", None)

        if len(authors) == 1:
            output.append(f"Author: {authors[0]}")
        elif 1 < len(authors) <= 5:
            output.append(f"Authors: {', '.join(authors)}")
        elif len(authors) > 5:
            output.append(f"Authors: {authors[0]} et al.")

        if metadata.get("date", None):
            output.append(f"Date: {metadata['date']}")

        tags = metadata.get("tags", None)

        if tags:
            output.append(self.format_tags(tags, is_tag_internal_link))
        return output


class ItemAnnotations(ZoteroItemBase):
    def __init__(self, item_key: str):
        super().__init__()
        self.item_key = item_key
        self.doc = Document(
            name="initial_filename"
        )  # the filename will be updated later!

    def format_highlight(self, highlight: Dict) -> str:
        data = highlight["data"]
        # zotero_unique_id = f"(key={highlight['key']}, version={highlight['version']})"
        return (
            f"{data['annotationText']} "
            f"(Page {data['annotationPageLabel']})"
            f"<!--(Highlighted on {data['dateAdded']})-->"
            # f"<!---->"
        )

    def create_metadata_section(self, metadata: Dict) -> None:
        self.doc.add_header(level=1, text="Metadata")
        self.doc.add_unordered_list(self.format_metadata(metadata))

    def create_highlights_section(self, highlights: List) -> None:
        self.doc.add_header(level=1, text="Highlights")
        self.doc.add_unordered_list(self.format_highlight(h) for h in highlights)

    def generate_output(self):
        d = group_annotations_by_parent_file(all_annotations)
        item_highlights = d[self.item_key]
        item_details = self.zotero.item(self.item_key)
        metadata = self.get_item_metadata(item_details)

        self.create_metadata_section(metadata)
        self.create_highlights_section(item_highlights)

        output_filename = metadata["title"]
        self.doc._name = output_filename
        self.doc.output_page()
        print(f"File {output_filename} is successfully created.")


# def create_md_doc(highlights, notes, metadata, frontmatter) -> None:

# item_key = "UIBHCUP6"
item_key = "N69RPVEF"

a = ItemAnnotations(item_key)
