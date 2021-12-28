from os import environ
from pathlib import Path

from pyzotero.zotero import Zotero

__version__ = "0.0.1"

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

zotero_client = Zotero(
    library_id=environ.get("ZOTERO_LIBRARY_ID", "123"),
    library_type="user",
    api_key=environ.get("ZOTERO_API_KEY", "userkey"),
)
