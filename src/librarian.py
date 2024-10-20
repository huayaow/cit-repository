"""
This script is used to manage the data files.
* Search new papers from DBLP and add them into an add.csv file (need further manual process)
* Update scholar.csv based on the current list.csv file 
"""
import csv
from dblp import DBLP

class Librarian:
  def __init__(self):
    self.dblp = DBLP()

    self.paper_list_filename = 'data/list.csv'
    self.paper_list_fields = ['year', 'type', 'author', 'title', 'field', 'tag', 
                        'booktitle', 'abbr', 'vol', 'no', 'pages', 'doi']  
    
    self.scholar_filename = 'data/scholar.csv'
    self.scholar_fields = ['id', 'name', 'institution', 'category', 'country', 'homepage']

    # get the list of current papers
    with open(self.paper_list_filename, 'r') as file:
      reader = csv.DictReader(file)
      self.papers = list(reader)
    # get the list of current scholars
    with open(self.scholar_filename, 'r') as file:
      reader = csv.DictReader(file)
      self.scholar = list(reader)
    print('[librarian] load {} papers from "{}"'.format(len(self.papers), self.paper_list_filename))
    print('            load {} scholars from "{}"'.format(len(self.scholar), self.scholar_filename))

  def search_new_papers(self, year, output_file='data/add.csv'):
    """
    Search DBLP and write new papers found into a file. Note that this often contain papers 
    that are irrelevant to CIT.
    """
    # these paper titles are already included in repository
    paper_titles = [e['title'] for e in self.papers]

    # these paper titles should be excluded
    with open('data/excluded.txt', 'r') as f:
      excluded_titles = [e.strip() for e in f.readlines()]

    # search dblp for new papers
    new_papers = self.dblp.search_paper(already_have=paper_titles, 
                                        excluded=excluded_titles,
                                        after_year=year)
    
    # write the new papers into the csv file
    with open(output_file, 'w', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=self.paper_list_fields)
      writer.writeheader()
      for each in new_papers:
        writer.writerow(each)

    print('[librarian] write {} papers to "{}" (might be irrelevant to CIT)'.format(
      len(new_papers), output_file))

  def update_scholar(self):
    """
    Update scholar.csv accoridng to list.csv
    """
    current_names = [e['name'] for e in self.scholar]
    paper_names = []
    new_names = []

    # for each paper authors
    for each in self.papers:
      names = each['author'].split(', ')
      for name in names:
        paper_names.append(name)
        if name not in current_names:
          new_names.append(name)
    print('[librarian] found {} new scholar names'.format(len(new_names)))

    for each in current_names:
      if each not in paper_names:
        print('\tnot appear in paper list: ' + each)

    if len(new_names) > 0:
      # add these names into scholar.csv
      with open(self.scholar_filename, 'a') as file:
        id = len(current_names) + 1
        writer = csv.DictWriter(file, fieldnames=self.scholar_fields)
        for each in new_names:
          writer.writerow({'id': id, 'name': each, 
                          'institution': '', 'category': '', 'country': '', 'homepage': ''})
      print('[librarian] succesfully write new scholars')

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
  # lib.search_new_papers(2018)
  lib.update_scholar()
