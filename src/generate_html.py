import csv
import json
import shutil
import pandas as pd
from bs4 import BeautifulSoup
from papers import Paper

class Generator:
  def __init__(self):
    self.list_filename = 'data/list.csv'
    self.scholar_filename = 'data/scholar.csv'
    self.statistics_filename = 'data/statistics.json'

    # read all papers from the csv file
    self.papers = []
    with open(self.list_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Paper(each)
        self.papers.append(p)
    
    # read all scholars from the csv file
    self.scholars = []
    with open(self.scholar_filename, 'r') as file:
      for each in csv.DictReader(file):
        self.scholars.append(each)
    
    # get statistics data 
    with open(self.statistics_filename) as file:
      self.data = json.load(file)

    print('[GenHTML] read {} papers and {} scholars'.format(len(self.papers), len(self.scholars)))

  def generate_index(self, date):
    """
    Generate the static index.html file. Need to reaplce the followings:
    * Description of the sub-title <- last update date
    * Statistics <- number of papers, [TODO: scholars, institutions]
    * Chart bar <- cumulative number of publications (with date)
    * Chart pie <- distribution of research topics
    """
    # update the HTML file 
    with open('pages/_index.html', 'r') as file:
      soup = BeautifulSoup(file.read(), 'html.parser')
    
    # description and statistics
    element = soup.find(id='replace-description')
    element.string = 'Collection of Research Papers of CIT (Last Update in {})'.format(date)
    element = soup.find(id='replace-number-1')
    element.string = '{}'.format(len(self.papers))
    element = soup.find(id='replace-number-2')
    element.string = '{}'.format(len(self.scholars))
    element = soup.find(id='replace-bar-descrption')
    element.string = 'From 2000 to {}'.format(date.split()[-1])

    with open('index.html', 'w') as file:
      file.write(str(soup))
    
    # update the js file
    with open('assets/index-chart.js','r') as f:
      lines = f.readlines()
    
    # cumulative number of publications
    lines[6] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['cumulative']['year']]))
    lines[12] = '        data: {}\n'.format(str(self.data['cumulative']['value']))
    
    # distribution of research fields
    lines[46] = '        data: {},\n'.format(str(self.data['distribution']['count']))
    lines[50] = '    labels: [{}]\n'.format(', '.join(['"{}"'.format(e) for e in self.data['distribution']['fields']]))

    with open('assets/index-chart.js', 'w') as f:
      f.writelines(lines)

    print('[GenHTML] succesfully update list.html"')

  def generate_list(self):
    """
    Generate the static components/list.html file. Need to reaplce the followings:
    * Description of the sub-title <- number of papers
    * Data table <- complete paper list
    """
    # update the HTML file 
    with open('pages/_list.html', 'r') as file:
      soup = BeautifulSoup(file.read(), 'html.parser')

    # replace "XX papers included"
    element = soup.find(id='replace-description')
    element.string = '{} papers included'.format(len(self.papers))

    # replace data table 
    element = soup.find(id='replace-paper-data-tbody')
    element.string = ''
    # print(element)

    # create a new row for each item in data and add this new row into the HTML table
    for each in self.papers:
      new_row = soup.new_tag('tr')
      name_cell = BeautifulSoup('<td>{}</td>'.format(each.year), 'html.parser')
      age_cell = BeautifulSoup(
        '<td><p>{}<br><strong>{}</strong><br><em>{}</em></p></td>'.format(
          each.author, each.title, each.venue_str()), 'html.parser')
      doi_cell = BeautifulSoup(
        '<td><a href="https://www.doi.org/{}" target="_blank">DOI</a></td>'.format(
          each.doi), 'html.parser')

      new_row.append(name_cell)
      new_row.append(age_cell)
      new_row.append(doi_cell)
      element.append(new_row)
      # print(element)

    with open('components/list.html', 'w') as file:
      file.write(str(soup))
    
    print('[GenHTML] succesfully add {} rows into "components/list.html"'.format(len(self.papers)))

  def generate_statistics(self):
    """
    Generate the statistics page. Need to reaplce the followings:
    * Chart line <- annual number of publications
    * [TODO] Chart line <- annual number of publications of each field
    * [TODO] Chart word cloud <- title
    * [TODO] Chart pie <- distribution of scholars accross the world
    """    
    # update the HTML file
    shutil.copyfile('pages/_statistics.html', 'components/statistics.html')

    # update the js file
    with open('assets/statistics-chart.js','r') as f:
      lines = f.readlines()

    # annual number of publications
    lines[5] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['annual']['year']]))
    lines[11] = '        data: {}\n'.format(str(self.data['annual']['value']))

    with open('assets/statistics-chart.js', 'w') as f:
      f.writelines(lines)

    print('[GenHTML] succesfully update statistics.html"')

if __name__ == '__main__':
  g = Generator()
  g.generate_index(date='Nov 2024')
  g.generate_list()
  g.generate_statistics()
