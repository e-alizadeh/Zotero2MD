from zotero2md import zotero_client
from zotero2md.utils import group_annotations_by_parent_file, retrieve_all_annotations
from zotero2md.zotero import ItemAnnotations

if __name__ == "__main__":
    highlights = group_annotations_by_parent_file(
        retrieve_all_annotations(zotero_client)
    )

    for i, item_key in enumerate(highlights.keys()):
        print(f"File {i + 1} of {len(highlights)} is under process ...")
        item = ItemAnnotations(item_annotations=highlights[item_key], item_key=item_key)
        item.generate_output()
        print("\n")
