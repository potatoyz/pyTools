# pyTools

This repository is a collection of small Python utilities:

- **ChangMDCodeBlockType** – batch update the language annotation for code blocks in Markdown files.  It can be used as a Python module or through a simple [PySimpleGUI](https://pysimplegui.readthedocs.io/) interface.
- **NovelDownloader** – a multi-threaded downloader for novels hosted on [soquwu.com](https://www.soquwu.com).  It scrapes chapter content and writes the novel to a local text file.

## ChangMDCodeBlockType

This tool walks through a Markdown file and replaces the language marker after the opening triple backticks with a user provided value.

### Usage

Run the GUI:

```bash
python ChangMDCodeBlockType/gui.py
```

Select the Markdown files to process and choose the desired language from the dropdown.

## NovelDownloader

`NovelDownloader/download_novel.py` fetches novels from **soquwu.com**.  It prompts for the directory page of a novel, retrieves the list of chapters, and downloads them concurrently using threads.

The resulting text file is written under the `novels/` directory.

### Requirements

- `bs4`
- `lxml`
- Internet connectivity to the target site

Run with:

```bash
python NovelDownloader/download_novel.py
```

## Development

The scripts were created as utilities and contain no formal test suite.  Python files compile without errors:

```bash
python -m py_compile ChangMDCodeBlockType/change.py ChangMDCodeBlockType/gui.py NovelDownloader/download_novel.py
```


