from argparse import ArgumentParser

from zotero2md.zt2md import Zotero2Markdown

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

    zt = Zotero2Markdown(
        zotero_key=args["zotero_key"],
        zotero_library_id=args["zotero_user_id"],
        zotero_library_type=args["library_type"],
        params_filepath=args.get("config_filepath", None),
        include_annotations=True,
        include_notes=True,
    )

    zt.run_all()
    zt.save_failed_items_to_txt("failed_zotero_items.txt")
