import json
from typing import Dict, List, Tuple, Union

from snakemd import Document, MDList, Paragraph

from zotero2md import ROOT_DIR, zotero_client
from zotero2md.utils import sanitize_tag

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
        self.zotero = zotero_client

        # Load output configurations used for generating markdown files.
        with open(ROOT_DIR.joinpath("output_config.json"), "r") as f:
            self.md_config = json.load(f)

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

    def format_tags(self, tags: List[Dict[str, str]]) -> str:
        flattened_tags = [d_["tag"] for d_ in tags]
        if self.md_config["convertTagsToInternalLinks"]:
            return " ".join(
                [
                    f"#{sanitize_tag(tag)}"
                    if tag in self.md_config["doNotConvertFollowingTagsToLink"]
                    else f"[[{tag}]]"
                    for tag in flattened_tags
                ]
            )
        else:
            return " ".join([f"#{sanitize_tag(tag)}" for tag in flattened_tags])

    def format_metadata(self, metadata: Dict) -> List:
        output: List = []
        authors = metadata.get("creators", None)
        if authors:
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
    def __init__(self, item_annotations: List[Dict], item_key: str):
        super().__init__()
        self.item_annotations = item_annotations
        self.item_key = item_key
        self.item_details = self.zotero.item(self.item_key)

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
        tags = data["tags"]
        # zotero_unique_id = f"(key={highlight['key']}, version={highlight['version']})"
        annot_text = ""
        annot_sub_bullet = []
        if data["annotationType"] == "note":
            annot_text = (
                f"{data['annotationComment']} (Note on *Page {data['annotationPageLabel']}*)"
                + self._format_highlighted_date(data["dateModified"])
                # f"<!---->"
            )
        elif data["annotationType"] == "highlight":
            annot_text = (
                f"{data['annotationText']} "
                f"(*Page {data['annotationPageLabel']}*)"
                f"<!--(Highlighted on {data['dateAdded']})-->"
                # f"<!---->"
            )
            if data.get("annotationComment", "") != "":
                annot_sub_bullet.append(f"**Comment**: {data['annotationComment']}")

        if tags:
            annot_sub_bullet.append(self.format_tags(tags))

        return annot_text, MDList(annot_sub_bullet)

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
        metadata = self.get_item_metadata(self.item_details)

        self.create_metadata_section(metadata)
        self.create_annotations_section(self.item_annotations)

        output_filename = metadata["title"]
        self.doc._name = output_filename
        try:
            self.doc.output_page("zotero_output")
            print(
                f'File "{output_filename}" (item_key="{self.item_key}") was successfully created.'
            )
        except:
            print(
                f'File "{output_filename}" (item_key="{self.item_key}") is failed to generate.\n'
                f"SKIPPING..."
            )
