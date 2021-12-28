from typing import Dict, List, Tuple, Union

from pyzotero.zotero import Zotero
from snakemd import Document, MDList, Paragraph

from zotero2md import default_params
from zotero2md.utils import sanitize_tag


class ZoteroItemBase:
    def __init__(self, zotero_client: Zotero, md_params: Dict = None):
        self.zotero = zotero_client

        # Load output configurations used for generating markdown files.
        self.md_config = default_params

        if md_params:
            self.md_config = {**self.md_config, **md_params}

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
                    if tag in self.md_config["doNotConvertFollowingTagsToLink"]  # type: ignore
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
    def __init__(
        self,
        zotero_client: Zotero,
        md_params: Union[Dict, None],
        item_annotations: List[Dict],
        item_key: str,
    ):
        super().__init__(zotero_client, md_params)
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
        """Generate the metadata sections (titled "Metadata") containing metadata about the Zotero Item

        Parameters
        ----------
        metadata: Dict
            A dictionary of an item details

        Returns
        -------
        None
        """
        self.doc.add_header(level=1, text="Metadata")
        self.doc.add_element(MDList(self.format_metadata(metadata)))

    def create_annotations_section(self, annotations: List) -> None:
        """Generate the annotation sections (titled "Highlights")
        In Zotero, an annotation is a highlighted text with the possibility of having related comment and tag(s).
        In addition, a note can also be added to a page without any highlight. This is also considered an annotation.
        The itemType="annotation" in the API response of both scenarios above.

        Parameters
        ----------
        annotations: List[Dict]
            A list containing all annotations of a Zotero Item.

        Returns
        -------
        None
        """
        self.doc.add_header(level=1, text="Highlights")
        annots = []
        for h in annotations:
            formatted_annotation = self.format_annotation(h)
            if isinstance(formatted_annotation, tuple):
                annots.append(formatted_annotation[0])
                annots.append(formatted_annotation[1])
            else:
                annots.append(formatted_annotation)

        self.doc.add_element(MDList(annots))

    def generate_output(self) -> Union[None, Tuple[str, str]]:
        """Generate the markdown file for a Zotero Item combining metadata, annotations

        Returns
        -------
        List
            Output (filename, item_key) of failed markdown files to compile.

        """
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
            return None
        except:
            print(
                f'File "{output_filename}" (item_key="{self.item_key}") is failed to generate.\n'
                f"SKIPPING..."
            )
            return output_filename, self.item_key
