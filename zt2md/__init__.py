from os import environ
from pathlib import Path

from pyzotero.zotero import Zotero

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

zotero_client = Zotero(
    library_id=environ["LIBRARY_ID"],
    library_type="user",
    api_key=environ["ZOTERO_API_KEY"],
)
