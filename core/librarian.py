"""
This script is used to manage the data files.
* Search new papers from DBLP and add them into an add.csv file.
* Update scholar.csv and paper.csv based on the latest data.
* Generate the statistics.json file (via jupyter notebook).
"""
import csv
import subprocess
import pandas as pd
from dblp import DBLP

class Librarian:
  def __init__(self):
    self.dblp = DBLP()

    self.paper_filename = 'data/paper.csv'
    self.paper_fields = ['year', 'type', 'author', 'title', 'field', 'tag', 
                         'booktitle', 'abbr', 'vol', 'no', 'pages', 'doi']  
    
    self.scholar_filename = 'data/scholar.csv'
    self.scholar_fields = ['id', 'name', 'institution', 'country', 'homepage']
    self.target_venues = ['TSE', 'TOSEM', 'EMSE', 'JSS', 'IST', 'ICSE', 'FSE', 'ASE', 
                          'ISSTA', 'SANER', 'ISSRE', 'ICST', 'ICSTW']

    self.keywords = [
      'combinatorial testing',         
      'covering array', 
      'combinatorial test', 
      't-wise coverage'
    ]

    # get the list of current papers
    self.paper = pd.read_csv(self.paper_filename, sep=',', header=0)
    print('🤖 load {} papers from {}'.format(self.paper.shape, self.paper_filename))

    # get the list of current scholars
    self.scholar = pd.read_csv(self.scholar_filename, sep=',', header=0)
    print('🤖 load {} scholars from {}'.format(self.scholar.shape, self.scholar_filename))
  
  def search_new_papers(self, keywords=None, after_year=None, output_file='data/add.csv'):
    """
    Search DBLP and add new papers found into a file. Note that this often contain papers 
    that are irrelevant to CIT.
    """
    # these paper titles are already included in repository
    included_titles = self.paper['title'].str.lower().tolist()

    # these paper titles should be excluded
    with open('core/excluded/format.txt', 'r') as file:
      excluded_titles = [e.strip().lower() for e in file.readlines()]
    with open('core/excluded/irrelevant.txt', 'r') as file:
      excluded_titles += [e.strip().lower() for e in file.readlines()]

    # search dblp for new papers
    keywords = self.keywords if keywords == None else keywords
    new_papers = self.dblp.search_paper(keywords=keywords,
                                        already_have=included_titles, 
                                        excluded=excluded_titles,
                                        after_year=after_year)
    
    # write the new papers into the add.csv file
    with open(output_file, 'w', encoding='utf-8') as file:
      writer = csv.DictWriter(file, fieldnames=self.paper_fields)
      writer.writeheader()
      for each in new_papers:
        writer.writerow(each)

    print('🤖 add {} papers to {} (might be irrelevant to CIT)'.format(len(new_papers), output_file))

  def update_table(self):
    """
    Update scholar.csv
      1. if the name appears in paper.csv but not in scholar.csv, add it into scholar.csv
      2. calculate the number of papers published in target venues for each scholar
    Update paper.csv
      1. sort by year, booktitle, and title
    """
    # names appear in paper table but not in scholar table
    current_names = self.scholar['name'].tolist()
    new_names = []

    # number of authored papers for each scholar, in the format of
    # {'Yu Lei': {'ICSTW': 31, 'ASE': 2, 'TSE': 8, 'ISSRE': 1, 'ICST': 3}}
    paper_count = {}

    for row in self.paper.itertuples(index=False):
      names = row.author.split(', ')
      # check whether a new name appears
      for name in names:
        if name not in current_names:
          new_names.append(name)
      # calculate number of authored papers (for target venues only)
      if row.abbr in self.target_venues:
        for name in names:
          if name not in paper_count:
            paper_count[name] = {}
          elif row.abbr not in paper_count[name]:
            paper_count[name][row.abbr] = 1
          elif row.abbr in paper_count[name]:
            paper_count[name][row.abbr] += 1
          else:
            print('🤖 update scholar error: {}'.format(row))
            return

    # add new names into scholar.csv
    last_id = self.scholar['id'].max()
    for each in new_names:
      last_id = last_id + 1
      new_row = pd.DataFrame([{'id': last_id, 'name': each}])
      self.scholar = pd.concat([self.scholar, new_row], ignore_index=True)
    print('🤖 found {} new scholar names: {}'.format(len(new_names), new_names))

    # zero all paper numbers and update them
    self.scholar.iloc[:, 5:5 + len(self.target_venues)] = 0
    cols = self.scholar.columns[5:5 + len(self.target_venues)]
    self.scholar[cols] = self.scholar[cols].astype('int64')

    for name in paper_count:
      for abbr in paper_count[name]:
        self.scholar.loc[self.scholar['name'] == name, abbr] = paper_count[name][abbr]

    # remove duplicate names
    # self.df_scholar = self.df_scholar.drop_duplicates(subset=['name'])

    # save the updated scholar.csv
    self.scholar.to_csv(self.scholar_filename, sep=',', encoding='utf-8', index=False, header=True)
    print('🤖 update scholar.csv')

    # sort paper.csv
    self.paper = self.paper.sort_values(['year', 'booktitle', 'title'], ascending=False)
    self.paper.to_csv(self.paper_filename, sep=',', encoding='utf-8', index=False, header=True)
    print('🤖 update paper.csv')

  def check_paper(self, filename, start=None, end=None):
    """
    Determine whether the paper titles listed in the file are included in DBLP.
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

  def update_statistic(self):
    """
    Generate the statistic.json file for drawing figures
    """
    subprocess.run('jupyter nbconvert --to notebook --inplace --execute core/analysis.ipynb', shell=True)    
    print('🤖 generate the "statistic.json" and "rank.csv" files')

    subprocess.run('jupyter nbconvert --to notebook --inplace --execute core/analysis_network.ipynb', shell=True)
    print('🤖 generate the "co-authorship network" related files')

if __name__ == '__main__':
  lib = Librarian()
  # lib.search_new_papers()
  lib.update_table()
  lib.update_statistic()
