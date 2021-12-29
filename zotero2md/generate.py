from argparse import ArgumentParser
from typing import Union

from pyzotero.zotero import Zotero

from zotero2md.utils import group_annotations_by_parent_file
from zotero2md.zotero import (
    ItemAnnotations,
    get_zotero_client,
    retrieve_all_annotations,
)


def generate_annotations_for_all_items(
    zotero_client: Zotero, params_filepath: Union[str, None] = None
) -> None:
    highlights = group_annotations_by_parent_file(
        retrieve_all_annotations(zotero_client)
    )

    failed_files = []
    for i, item_key in enumerate(highlights.keys()):
        print(f"File {i + 1} of {len(highlights)} is under process ...")
        item = ItemAnnotations(
            zotero_client=zotero_client,
            params_filepath=params_filepath,
            item_annotations=highlights[item_key],
            item_key=item_key,
        )
        out = item.generate_output()
        if out:
            failed_files.append(out)
        print("\n")

    if failed_files:
        print("\nItems that failed to compile to a markdown file:")
        for (file, item_key) in failed_files:
            print(f"Item Key: {item_key} | File: {file}\n")
    else:
        print("\nAll items were successfully created!")


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate Markdown files")
    parser.add_argument(
        "zotero_key", help="Zotero API key (visit https://www.zotero.org/settings/keys)"
    )
    parser.add_argument(
        "zotero_user_id",
        help="Zotero User ID (visit https://www.zotero.org/settings/keys)",
    )
    parser.add_argument(
        "--library_type",
        default="user",
        help="Zotero Library type ('user': for personal library (default value), 'group': for a shared library)",
    )
    parser.add_argument(
        "--config_filepath",
        type=str,
        help="Filepath to a .json file containing the path",
    )

    args = vars(parser.parse_args())

    # ----- Create a Zotero client object
    zot_client = get_zotero_client(
        user_id=args["zotero_user_id"],
        library_type=args["library_type"],
        api_key=args["zotero_key"],
    )

    generate_annotations_for_all_items(
        zot_client, params_filepath=args.get("config_filepath", None)
    )
