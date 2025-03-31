# Scripts

This directory includes code scripts for data management of the cit-repository.

### Paper Search and Data Management

Use `librarian.py` to search new papers and update data in the `data` directory:

*  `search_new_papers()` : Search new papers from DBLP. The new papers found will be written into an `add.csv` file (further manual processing is requried). 
* `update_scholar()`: Update the `scholar.csv`  file according to the `paper.csv` file.
* `update_paper()`: Reorder the `paper.csv` file.
* `update_statistics()`: Update the data in the `statistics.json` file. These data will be used for drawing charts in the web pages.

### Generate static HTML Pages

Use `generate_html.py` to generate the final static HTML pages for the repository:

* `generate_index()`: generate the `index.html` file.
* `generate_papers_list()`: generate the `components/paper.html` file.
* `generate_tools_list()`: generate the `components/tool.html` file.
* `generate_statistics()`: generate the `components/statistic.html` file.