from zt2md import all_annotations, all_notes
from zt2md.utils import group_annotations_by_parent_file
from zt2md.zotero import ItemAnnotations

if __name__ == "__main__":
    highlights = group_annotations_by_parent_file(all_annotations)
    notes = group_annotations_by_parent_file(all_notes)
    note = "WS2V4TWS"
    last_note = notes[note]
    # item_key = "UIBHCUP6" # HS553U65
    item_key = "HS553U65"

    a = ItemAnnotations(item_annotations=highlights[item_key], item_key=item_key)
    a.generate_output()
