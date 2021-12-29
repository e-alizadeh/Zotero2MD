import json
from os import environ
from pathlib import Path
from typing import Dict, List, Tuple, Union

from markdownify import markdownify
from pyzotero.zotero import Zotero
from pyzotero.zotero_errors import ParamNotPassed, UnsupportedParams
from snakemd import Document, MDList, Paragraph

from zotero2md import default_params
from zotero2md.utils import sanitize_filename, sanitize_tag

_OUTPUT_DIR = Path("zotero_output")
_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_zotero_client(
    library_id: str = None, api_key: str = None, library_type: str = "user"
) -> Zotero:
    """Create a Zotero client object from Pyzotero library

    Zotero userID and Key are available

    Parameters
    ----------
    library_id: str
        If not passed, then it looks for `ZOTERO_LIBRARY_ID` in the environment variables.
    api_key: str
        If not passed, then it looks for `ZOTERO_KEY` in the environment variables.
    library_type: str ['user', 'group']
        'user': to access your Zotero library
        'group': to access a shared group library

    Returns
    -------
    Zotero
        a Zotero client object
    """

    if library_id is None:
        try:
            library_id = environ["ZOTERO_LIBRARY_ID"]
        except KeyError:
            raise ParamNotPassed(
                "No value for library_id is found. "
                "You can set it as an environment variable `ZOTERO_LIBRARY_ID` or use `library_id` to set it."
            )

    if api_key is None:
        try:
            api_key = environ["ZOTERO_KEY"]
        except KeyError:
            raise ParamNotPassed(
                "No value for api_key is found. "
                "You can set it as an environment variable `ZOTERO_KEY` or use `api_key` to set it."
            )

    if library_type is None:
        library_type = environ.get("LIBRARY_TYPE", "user")
    elif library_type not in ["user", "group"]:
        raise UnsupportedParams("library_type value can either be 'user' or 'group'.")

    return Zotero(
        library_id=library_id,
        library_type=library_type,
        api_key=api_key,
    )


class ZoteroItemBase:
    def __init__(
        self,
        zotero_client: Zotero,
        item_key: str,
        params_filepath: Union[str, None] = None,
    ):
        self.zotero = zotero_client
        self.item_key = item_key
        self.item_details = self.zotero.item(self.item_key)
        self.parent_item_key = self.item_details["data"].get("parentItem", None)

        # Load output configurations used for generating markdown files.
        self.md_config = default_params

        if params_filepath:
            with open(Path(params_filepath), "r") as f:
                params = json.load(f)
            self.md_config = {**self.md_config, **params}

    def get_item_metadata(self) -> Dict:
        if self.parent_item_key:
            top_parent_item = self.zotero.item(self.parent_item_key)
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
            data = self.item_details["data"]
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


class ItemAnnotationsAndNotes(ZoteroItemBase):
    def __init__(
        self,
        zotero_client: Zotero,
        item_key: str,
        item_annotations: List[Dict] = None,
        item_notes: List[Dict] = None,
        params_filepath: Union[str, None] = None,
    ):
        """
        Assumptions
        -----------
        item_annotations and item_notes belong to the same Zotero item!

        Parameters
        ----------
        zotero_client
        item_key
        item_annotations
        item_notes
        params_filepath
        """
        super().__init__(zotero_client, item_key, params_filepath)
        self.item_annotations = item_annotations
        self.item_notes = item_notes

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
                f"{data['annotationComment']} (Note on *Page {data['annotationPageLabel']}*) "
                + self._format_highlighted_date(data["dateModified"])
                # f"<!---->"
            )
        elif data["annotationType"] == "highlight":
            annot_text = (
                f"{data['annotationText']} (*Page {data['annotationPageLabel']}*) "
                + self._format_highlighted_date(data["dateModified"])
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

    def format_note(self, note) -> Tuple[str, MDList]:
        data = note["data"]
        tags = data["tags"]

        md_note = markdownify(data["note"])
        note_sub_bullet = []

        if tags:
            note_sub_bullet.append(self.format_tags(tags))

        return md_note, MDList(note_sub_bullet)

    def create_notes_section(self, notes: List) -> None:
        self.doc.add_header(level=1, text="Notes")
        annots = []
        for note in notes:
            formatted_note = self.format_note(note)
            if isinstance(formatted_note, tuple):
                annots.append(formatted_note[0])
                annots.append(formatted_note[1])
            else:
                annots.append(formatted_note)

        self.doc.add_element(MDList(annots))

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
        metadata = self.get_item_metadata()
        title = metadata["title"]

        self.doc.add_header(title, level=1)
        self.create_metadata_section(metadata)
        if self.item_notes:
            self.create_notes_section(self.item_notes)
        if self.item_annotations:
            self.create_annotations_section(self.item_annotations)

        output_filename = sanitize_filename(title) + ".md"
        try:
            with open(_OUTPUT_DIR.joinpath(output_filename), "w+") as f:
                f.write(self.doc.render())
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


def retrieve_all_annotations(zotero_client: Zotero) -> List[Dict]:
    print(
        "Retrieving ALL annotations from Zotero Database. \nIt may take some time...\n"
    )
    return zotero_client.everything(zotero_client.items(itemType="annotation"))


def retrieve_all_notes(zotero_client: Zotero) -> List[Dict]:
    print("Retrieving ALL notes from Zotero Database. \nIt may take some time...\n")
    return zotero_client.everything(zotero_client.items(itemType="note"))
