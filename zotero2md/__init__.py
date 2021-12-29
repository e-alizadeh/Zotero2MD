from pathlib import Path

__author__ = "Essi Alizadeh"
__version__ = "0.1.0"

ROOT_DIR: Path = Path(__file__).parent
TOP_DIR: Path = ROOT_DIR.parent

default_params = {
    "convertTagsToInternalLinks": True,
    "doNotConvertFollowingTagsToLink": [],
    "includeHighlightDate": True,
    "hideHighlightDateInPreview": False,
}
