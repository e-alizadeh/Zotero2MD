import json
from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pyzotero.zotero import Zotero

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

ALL_ANNOTATIONS_FILEPATH = TOP_DIR.joinpath("all_annotations.json")
ALL_NOTES_FILEPATH = TOP_DIR.joinpath("all_notes.json")

load_dotenv(TOP_DIR.joinpath("secrets.env"))

zotero_client = Zotero(
    library_id=environ["LIBRARY_ID"],
    library_type="user",
    api_key=environ["ZOTERO_API_KEY"],
)

all_annotations = zotero_client.everything(zotero_client.items(itemType="annotation"))
all_notes = zotero_client.everything(zotero_client.items(itemType="note"))
# all_items = zotero.everything(zotero.all_top())

with open(ALL_ANNOTATIONS_FILEPATH, "r") as f:
    all_annotations = json.load(f)
with open(ALL_NOTES_FILEPATH, "r") as f:
    all_notes = json.load(f)
