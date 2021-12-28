import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, Optional, Union

from pyzotero.zotero import Zotero

from zotero2md.utils import group_annotations_by_parent_file, retrieve_all_annotations
from zotero2md.zotero import ItemAnnotations

parser = ArgumentParser(description="Generate Markdown files")
parser.add_argument(
    "zotero_key", help="Zotero API key (visit https://www.zotero.org/settings/keys)"
)
parser.add_argument(
    "zotero_user_id", help="Zotero User ID (visit https://www.zotero.org/settings/keys)"
)
parser.add_argument(
    "--config_filepath", type=str, help="Filepath to a .json file containing the path"
)

args = vars(parser.parse_args())


def generate_annotations_for_all_items(
    zotero_client: Zotero, output_params: Optional[Union[Dict, None]] = None
) -> None:
    highlights = group_annotations_by_parent_file(
        retrieve_all_annotations(zotero_client)
    )

    failed_files = []
    for i, item_key in enumerate(highlights.keys()):
        print(f"File {i + 1} of {len(highlights)} is under process ...")
        item = ItemAnnotations(
            zotero_client=zotero_client,
            md_params=output_params,
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
        print("\n All items were successfully created!")


if __name__ == "__main__":
    zotero_client = Zotero(
        library_id=args["zotero_user_id"],
        library_type="user",
        api_key=args["zotero_key"],
    )

    if args.get("config_filepath", None):
        config_filepath = Path(args["config_filepath"])
        with open(config_filepath, "r") as f:
            params = json.load(f)
    else:
        params = None

    generate_annotations_for_all_items(zotero_client, output_params=params)
