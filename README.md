# cit-repository

The **cit-repository** aims to provide a full coverage of publications in the literature of combinatorial interaction testing, and analyzes the status and developement of this research field.

### Data

The `data` directory contains primary data of this repository, including:
* `paper.csv`: a list of publications
* `scholar.csv`: a list of scholars
* `statistic.json`: data for drawing figures
* `tool.csv`: a collection of testing tools

### Usage

1. Run `python core/repository.py search [--after=year]` to search new papers (from DBLP). 

   After this step, need to perform manual processing on the newly generated `add.csv` file to **filter out irrelvant papers**, and also **determine research field of each new paper**. Then, all new papers should be manually copied into the `paper.csv` file.

2. Run `python core/repository.py update --date='current date'` to update repository data (based on the content in `paper.csv`), and also generate static HTML pages.
