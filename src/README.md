# Scripts

This directory includes code scripts for data management of the cit-repository.

## Paper Search and Data Management

Use `librarian.py` to search new papers and update data in the `data` directory. The primay functions include:

*  `search_new_papers()` : Search new papers from DBLP. 

  The new papers found will be written into an `add.csv` file. After this step, need to perform manual processing to **filter out irrelvant papers**, and also **determine research field of each new paper**. Then, all new papers should be manually copied into the `list.csv` file.

* `update_scholar()`: Update the scholar data file according to the current `list.csv` file.
* `update_statistics()`: Update the data in the `statistics.json` file. These data will be used for drawing charts in the web pages.

## Generate static HTML Files

Use `generate_html.py` to generate the final static HTML pages for the repository. The primary functions include:

* `generate_index()`: generate the `index.html` file.
* `generate_list()`: generate the `components/list.html` file.
* `generate_statistics()`: generate the `components/statistics.html` file.