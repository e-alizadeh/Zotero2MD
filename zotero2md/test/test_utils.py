from zotero2md.utils import sanitize_tag


def test_sanitize_tag():
    assert sanitize_tag("AB CD") == "AB_CD"
    assert sanitize_tag("AB_-CD") == "AB_-CD"
    assert sanitize_tag(" a b ") == "a_b"
