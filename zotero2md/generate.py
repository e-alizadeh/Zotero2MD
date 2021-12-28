from zotero2md import zotero_client
from zotero2md.utils import group_annotations_by_parent_file, retrieve_all_annotations
from zotero2md.zotero import ItemAnnotations

if __name__ == "__main__":
    highlights = group_annotations_by_parent_file(
        retrieve_all_annotations(zotero_client)
    )

    failed_files = []
    for i, item_key in enumerate(highlights.keys()):
        print(f"File {i + 1} of {len(highlights)} is under process ...")
        item = ItemAnnotations(item_annotations=highlights[item_key], item_key=item_key)
        out = item.generate_output()
        if out:
            failed_files.append(out)
        print("\n")

    if failed_files:
        print("\nItems that failed to compile to a markdown file:")
        for (file, item_key) in failed_files:
            print(f"Item Key: {item_key} | File: {file}\n")
    else:
        print("\n All items were successfully created!")
