# Zotero to Markdown

Generate Markdown files from Zotero annotations and notes. 
With new [Zotero PDF Reader](https://www.zotero.org/support/pdf_reader_preview), all highlights are saved in the Zotero database.
The highlights are NOT saved in the PDF file unless you export the highlights in order to save them.

If you annotate your files outside the new Zotero PDF reader, this library will not work with your PDF annotations as those are not retrievable from Zotero API.
In that case, you may want to use zotfile + mdnotes to extract the annotations and convert them into markdown files.

**_This library is for you if you annotate (highlight + note) using the Zotero's PDF reader (including the Zotero iOS)_**

# Installation 
You can install the library by running 
```shell
pip install zotero2md
```

Note: If you do not have pip installed on your system, you can follow the instructions [here](https://pip.pypa.io/en/stable/installation/).

# Usage
Since we have to retrieve the notes from Zotero API, the minimum requirements are:
* **Zotero API key** [Required]: Create a new Zotero Key from [your Zotero settings](https://www.zotero.org/settings/key)
* **Zotero personal or group ID** [Required]: 
    * Your **personal library ID** (aka **userID**) can be found [here](https://www.zotero.org/settings/key) next to `Your userID for use in API calls is XXXXXX`.
    * If you're using a **group library**, you can find the library ID by 
        1. Go to `https://www.zotero.org/groups/`
        2. Click on the interested group.
        3. You can find the library ID from the URL link that has format like *https://www.zotero.org/groups/<group_id>/group_name*. The number between `/groups/` and `/group_name` is the libarry ID. 
* **Zotero library type** [Optional]: *"user"* (default) if using personal library and *"group"* if using group library.

Note that if you want to retrieve annotations and notes from a group, you should provide the group ID (`zotero_library_id=<group_id>`) and set the library type to group (`zotero_library_type="group"`).

## Approach 1 (Recommended)
After installing the library, open a Python terminal, and then execute the following:
```python 
from zotero2md.zt2md import Zotero2Markdown

zt = Zotero2Markdown(
    zotero_key="your_zotero_key",  
    zotero_library_id="your_zotero_id", 
    zotero_library_type="user", # "user" (default) or "group"
    params_filepath="",  # [Default values provided bellow] # The path to JSON file containing the custom parameters (See Section Custom Output Parameters).
    include_annotations=True, # Default: True
    include_notes=True, # Default: True
)
zt.run_all()
```
Just to make sure that all files are created, you can run `save_failed_items_to_txt()` to ensure that no file was 
was failed to create. If a file or more failed to create, the filename (item title) and the corresponding Zotero 
item key will be saved to a txt file. 
```python
zt.save_failed_items_to_txt("failed_zotero_items.txt")
```

## Approach 2
For this approach, you need to download `output_to_md.py` script. 
Run `python output_to_md.py -h` to get more information about all options. 
```shell
python zotero2md/output_to_md.py <zotero_key> <zotero_id>
```

For instance, assuming zotero_key=abcd and zotero_id=1234, you can simply run the following:
```shell
python zotero2md/output_to_md.py abcd 1234
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

# Features
- Generate MD files for all annotations and notes saved in Zotero
- The ability to convert Zotero tags to internal links (`[[ ]]`) used in many bidirectional MD editors.
  - You can even pass certain tags that you don't want to convert to internal links! (using `doNotConvertFollowingTagsToLink` parameter)

## Quick note
Since I'm personally using Obsidian as my markdown editor, there are custom parameters to generate MD files that are consistent with Obsidian and I'm planning to add more option there. 


# Roadmap
- [ ] Update existing annotations and notes
- [ ] Option to add frontmatter section (particularly useful for Obsidian)
- [ ] More flexibility in styling the output files 

# Request a new feature or report a bug
Feel free to request a new feature or report a bug in GitHub issue [here](https://github.com/e-alizadeh/Zotero2MD/issues).

## 📫 How to reach me:
<a href="https://ealizadeh.com" target="_blank"><img alt="Personal Website" src="https://img.shields.io/badge/Personal%20Website-%2312100E.svg?&style=for-the-badge&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/alizadehesmaeil/" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" /></a>
<a href="https://medium.com/@ealizadeh" target="_blank"><img alt="Medium" src="https://img.shields.io/badge/medium-%2312100E.svg?&style=for-the-badge&logo=medium&logoColor=white" /></a>
<a href="https://twitter.com/intent/follow?screen_name=es_alizadeh&tw_p=followbutton" target="_blank"><img alt="Twitter" src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" /></a>

<a href="https://www.buymeacoffee.com/ealizadeh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>