# CHANGELOG



<!--next-version-placeholder-->

## v0.2.0 (2022-01-01)
### Feature
* Define `Zotero2Markdown` class for easier implementation. Update failed item handling. Use Zotero2Markdown in `generate.py`. ([`1a461a5`](https://github.com/e-alizadeh/Zotero2MD/commit/1a461a569ebf17906e45b0858e84824b46d8ee00))

## v0.1.0 (2021-12-29)
### Feature
* Add notes to the output. Use markdownify library to convert HTML-styled notes to markdown. ([`3b83dc8`](https://github.com/e-alizadeh/Zotero2MD/commit/3b83dc82d47198010a136b4f9a06d744256e04ce))
* Pass config filepath to the ZoteroItemBase instead of the rendered dictionary. ([`af3e78e`](https://github.com/e-alizadeh/Zotero2MD/commit/af3e78eacddf036322ea29ab057677f45d0270a2))
* Add Argparser ([`935ce1a`](https://github.com/e-alizadeh/Zotero2MD/commit/935ce1ace737219eb9f73efe6e9e179beb116cfc))

### Fix
* Sanitize output filename and use it instead of output_page() method. ([`ba8da8d`](https://github.com/e-alizadeh/Zotero2MD/commit/ba8da8dc1b4b585dc8cd544500d025bd1ea43165))

### Documentation
* Update README. Add a section for custom output parameters. Add new line for better printouts. ([`0011d3a`](https://github.com/e-alizadeh/Zotero2MD/commit/0011d3a6b3ad3b40eaf319d834b5d065407156c0))
* Add docstrings to sanitize_tag() and sanitize_filename() ([`d08404d`](https://github.com/e-alizadeh/Zotero2MD/commit/d08404d70f4c5f0e220c978aa63fbe509ba6291c))
* Add docstrings to create_metadata_section. Add create_annotations_section() ([`ecc199e`](https://github.com/e-alizadeh/Zotero2MD/commit/ecc199e475bd362abbaca711981c98201640544a))

## v0.0.1 (2021-12-28)
First Release