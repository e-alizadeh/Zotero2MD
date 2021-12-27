import json
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

ALL_ANNOTATIONS_FILEPATH = TOP_DIR.joinpath("all_annotations.json")
ALL_NOTES_FILEPATH = TOP_DIR.joinpath("all_notes.json")

load_dotenv(TOP_DIR.joinpath("secrets.env"))

# all_annotations = zot.everything(zot.items(itemType="annotation"))
# all_notes = zot.everything(zot.items(itemType="note"))
# # all_items = zot.everything(zot.all_top())
#
# with open(ALL_ANNOTATIONS_FILEPATH, "w") as f:
#     json.dump(all_annotations, f)
#
# with open(ALL_NOTES_FILEPATH, "w") as f:
#     json.dump(all_notes, f)

with open(ALL_ANNOTATIONS_FILEPATH, "r") as f:
    all_annotations = json.load(f)
with open(ALL_NOTES_FILEPATH, "r") as f:
    all_notes = json.load(f)
