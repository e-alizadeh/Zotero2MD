import json
import os
from typing import Dict, List, Tuple, Union

from dotenv import load_dotenv
from pyzotero.zotero import Zotero
from snakemd import Document, MDList, Paragraph

# Load environment variables
from zt2md.utils import group_annotations_by_parent_file

load_dotenv("../secrets.env")

zot = Zotero(
    library_id=os.environ["LIBRARY_ID"],
    library_type="user",
    api_key=os.environ["ZOTERO_API_KEY"],
)
all_annotations = zot.everything(zot.items(itemType="annotation"))
all_notes = zot.everything(zot.items(itemType="note"))
# all_items = zot.everything(zot.all_top())

with open("../all_annotations.json", "w") as f:
    json.dump(all_annotations, f)

with open("../all_notes.json", "w") as f:
    json.dump(all_notes, f)

with open("../all_annotations.json", "r") as f:
    all_annotations = json.load(f)
with open("../all_notes.json", "r") as f:
    all_notes = json.load(f)

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
        self.md_config = {
            "convertTagToInternalLink": True,
            "doNotConvertTagsToLink": ["Machine Learning"],
            "includeHighlightDate": True,
            "hideHighlightDateInPreview": False,
        }

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

    def format_tags(self, tags: List[str]) -> str:
        if self.md_config["convertTagToInternalLink"]:
            return " ".join(
                [
                    f"[[{tag}]]"
                    if tag in self.md_config["doNotConvertTagsToLink"]
                    else f"#{tag}"
                    for tag in tags
                ]
            )
        else:
            return " ".join([f"#{tag}" for tag in tags])

    def format_metadata(self, metadata: Dict, is_tag_internal_link=True) -> List:
        output: List = []
        authors = metadata.get("creators", None)

        if len(authors) == 1:
            output.append(f"**Author:** {authors[0]}")
        elif 1 < len(authors) <= 5:
            output.append(f"**Authors:** {', '.join(authors)}")
        elif len(authors) > 5:
            output.append(f"**Authors:** {authors[0]} et al.")

        if metadata.get("date", None):
            output.append(f"**Date:** {metadata['date']}")

        tags = metadata.get("tags", None)

        if tags:
            output.append(self.format_tags(tags))
        return output


class ItemAnnotations(ZoteroItemBase):
    def __init__(self, item_key: str):
        super().__init__()
        self.item_key = item_key
        self.doc = Document(
            name="initial_filename"
        )  # the filename will be updated later!

    def _format_highlighted_date(self, date: str):
        if self.md_config["includeHighlightDate"]:
            if self.md_config["hideHighlightDateInPreview"]:
                return f"<!--(Highlighted on {date})-->"
            else:
                return f"(Highlighted on {date})"
        else:
            return ""

    def format_annotation(self, highlight: Dict) -> Union[Tuple, Paragraph]:
        data = highlight["data"]
        # zotero_unique_id = f"(key={highlight['key']}, version={highlight['version']})"
        if data["annotationType"] == "note":
            return Paragraph(
                f"{data['annotationComment']} (Note on Page {data['annotationPageLabel']})"
                + self._format_highlighted_date(data["dateModified"])
                # f"<!---->"
            )
        elif data["annotationType"] == "highlight":
            annot_text = Paragraph(
                f"{data['annotationText']} "
                f"(Page {data['annotationPageLabel']})"
                f"<!--(Highlighted on {data['dateAdded']})-->"
                # f"<!---->"
            )
            if data.get("annotationComment", "") == "":
                return annot_text
            else:
                annot_comment = MDList([f"**Comment**: {data['annotationComment']}"])
                return (annot_text, annot_comment)
        else:
            return Paragraph("")

    def create_metadata_section(self, metadata: Dict) -> None:
        self.doc.add_header(level=1, text="Metadata")
        self.doc.add_element(MDList(self.format_metadata(metadata)))

    def create_annotations_section(self, highlights: List) -> None:
        self.doc.add_header(level=1, text="Highlights")
        annots = []
        for h in highlights:
            formatted_annotation = self.format_annotation(h)
            if isinstance(formatted_annotation, tuple):
                annots.append(formatted_annotation[0])
                annots.append(formatted_annotation[1])
            else:
                annots.append(formatted_annotation)

        self.doc.add_element(MDList(annots))

    def generate_output(self):
        d = group_annotations_by_parent_file(all_annotations)
        item_highlights = d[self.item_key]
        item_details = self.zotero.item(self.item_key)
        metadata = self.get_item_metadata(item_details)

        self.create_metadata_section(metadata)
        self.create_annotations_section(item_highlights)

        output_filename = metadata["title"]
        self.doc._name = output_filename
        self.doc.output_page()
        print(f"File {output_filename} is successfully created.")


# def create_md_doc(highlights, notes, metadata, frontmatter) -> None:

if __name__ == "__main__":
    highlights = group_annotations_by_parent_file(all_annotations)
    notes = group_annotations_by_parent_file(all_notes)
    note = "WS2V4TWS"
    last_note = notes[note]
    # item_key = "UIBHCUP6"
    item_key = "N69RPVEF"

    a = ItemAnnotations(item_key)
    a.generate_output()
