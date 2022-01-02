from pathlib import Path

__author__ = "Essi Alizadeh"
__version__ = "0.2.0"

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

DEFAULT_PARAMS = {
    "convertTagsToInternalLinks": True,
    "doNotConvertFollowingTagsToLink": [],
    "includeHighlightDate": True,
    "hideHighlightDateInPreview": False,
}
