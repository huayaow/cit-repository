"""
This script is used to search new papers from DBLP, and add these papers into list.csv file.
"""
import json
import csv
from dblp import DBLP

class Librarian:
  def __init__(self):
    self.dblp = DBLP()
    self.data_filename = 'data/list.csv'
    self.data_fields = ['year', 'type', 'author', 'title', 'field', 'tag', 
                        'booktitle', 'abbr', 'vol', 'no', 'pages', 'doi']  
    # get the list of current papers
    with open(self.data_filename) as file:
      reader = csv.DictReader(file)
      self.data = list(reader)
    print('[librarian] load {} papers from "{}"'.format(len(self.data), self.data_filename))

  def search_new_papers(self, year, output_file='data/add.csv'):
    """
    Search DBLP and write new papers found into a file. Note that this often contain papers that
    are irrelevant to CIT.
    """
    # these paper titles are already included in repository
    paper_titles = [e['title'] for e in self.data]

    # search dblp for new papers
    new_papers = self.dblp.search_paper(already_have=paper_titles, after_year=year)
    
    # write the new papers into the csv file
    with open(output_file, 'w', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=self.data_fields)
      writer.writeheader()
      for each in new_papers:
        writer.writerow(each)

    print('[librarian] write {} papers to "{}" (might be irrelevant to CIT)'.format(
      len(new_papers), output_file))

  def check_paper_inclusion(self, filename, start=None, end=None):
    """
    Determine whether the papers (titles) listed in the file are included in DBLP.
    Each line in the file should be in the format of "index, title"
    """
    with open(filename, encoding='utf-8') as file:
      lines = file.readlines()

    for row, each in enumerate(lines):
      if (start is not None and row < start - 1) or (end is not None and row > end - 1):
        continue

      paper_title = each[each.find(',') + 1:].strip().lower()
      result, _ = self.dblp.check_paper(paper_title)
      if result == 'no_match':
        print('[{}] {}'.format(result, paper_title))

if __name__ == '__main__':
  lib = Librarian()
  lib.search_new_papers(2024)