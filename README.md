# Zotero to Markdown

Generate Markdown files from Zotero annotations (Zotero Beta). 
With new Zotero PDF Reader and Note Editor, all highlights are saved in Zotero databases.
The highlights are NOT saved in the PDF file unless you export the highlights in order to save them.

You can use the following commands to generate markdown files for your code


## Installation 
You can install the library by running 
```shell
pip install zotero2md
```

Note: If you do not have pip installed on your system, you can follow the instructions [here](https://pip.pypa.io/en/stable/installation/).


```shell
python zotero2md/generate.py <zotero_key> <zotero_id>
```

For instance, assuming zotero_key=abcd and zotero_id=1234, you can simply run the following:
```shell
python zotero2md/generate.py abcd 1234
```


## Custom Output Parameters
You can change default parameters by passing the `--config_filepath` option with the path to a
JSON file containing the desired configurations. For instance,

```shell
python zotero2md/generate.py <zotero_key> <zotero_id> --config_filepath ./sample_params.json
```

| Parameter                         | type            | default value |
|-----------------------------------|-----------------|---------------|
| `convertTagsToInternalLinks`      | bool            | true          |
| `doNotConvertFollowingTagsToLink` | List of strings | \[ \]         |
| `includeHighlightDate`            | bool            | true          |
| `hideHighlightDateInPreview`      | bool            | true          |


Any parameter in the JSON file will override the default setting. 
If a parameter is not provided, then the default value will be used. 

For example, if you don't want to show the highlight date in the output file, you can simply pass
a JSON file with the following content:
```json
{
  "hideHighlightDateInPreview": false
}
```

<a href="https://www.buymeacoffee.com/ealizadeh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>