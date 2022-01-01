from typing import Dict, List, Union

from zotero2md.utils import group_by_parent_item
from zotero2md.zotero import (
    ItemAnnotationsAndNotes,
    get_zotero_client,
    retrieve_all_annotations,
    retrieve_all_notes,
)


class Zotero2Markdown:
    def __init__(
        self,
        zotero_key: str,
        zotero_library_id: str,
        zotero_library_type: str = "user",
        params_filepath: str = None,
        include_annotations: bool = True,
        include_notes: bool = True,
    ):

        self.zotero_client = get_zotero_client(
            library_id=zotero_library_id,
            library_type=zotero_library_type,
            api_key=zotero_key,
        )
        self.config_filepath = params_filepath
        self.include_annots = include_annotations
        self.include_notes = include_notes
        self.failed_items: List[str] = []

    def run_all(self, params_filepath: Union[str, None] = None) -> None:
        annots_grouped: Dict = {}
        notes_grouped: Dict = {}
        if self.include_annots:
            annots_grouped = group_by_parent_item(
                retrieve_all_annotations(self.zotero_client)
            )
        if self.include_notes:
            notes_grouped = group_by_parent_item(retrieve_all_notes(self.zotero_client))

        for i, item_key in enumerate(annots_grouped.keys()):
            item = self.zotero_client.item(item_key)
            parent_item_key = item["data"].get("parentItem", None)
            print(f"File {i + 1} of {len(annots_grouped)} is under process ...")
            zotero_item = ItemAnnotationsAndNotes(
                zotero_client=self.zotero_client,
                params_filepath=params_filepath,
                item_annotations=annots_grouped[item_key],
                item_notes=notes_grouped.get(parent_item_key, None),
                item_key=item_key,
            )
            # del notes[parent_item_key]

            if zotero_item.failed_item:
                self.failed_items.append(zotero_item.failed_item)
            else:
                zotero_item.generate_output()

        # for i, item_key in enumerate(notes.keys()):
        #     print(f"File {i + 1} of {len(highlights)} is under process ...")
        #     item = ItemAnnotationsAndNotes(
        #         zotero_client=zotero_client,
        #         params_filepath=params_filepath,
        #         item_annotations=None,
        #         item_notes=notes[item_key],
        #         item_key=item_key,
        #     )
        #     out = item.generate_output()
        #     if out:
        #         failed_files.append(out)
        #     print("\n")

    def save_failed_items_to_txt(self, txt_filepath: str = ""):
        if txt_filepath == "":
            txt_filepath = "failed_zotero_items.txt"

        if self.failed_items:
            print(
                f"\n {len(self.failed_items)} markdown files (with all their annotations and notes) failed to create."
            )
            with open(txt_filepath, "w") as f:
                file_content = "\n".join(self.failed_items)
                f.write(file_content)
            print(f"List of all failed items are saved into {txt_filepath}")
        else:
            print("No failed item")
