import csv
import json
import shutil
import pandas as pd
from bs4 import BeautifulSoup
from papers import Paper
from tools import Tool

class Generator:
  def __init__(self):
    self.paper_filename = 'data/paper.csv'
    self.scholar_filename = 'data/scholar.csv'
    self.tools_filename = 'data/tool.csv'
    self.statistics_filename = 'data/statistic.json'

    # static files to be generated
    self.target_index = 'index.html'
    self.target_index_js = 'assets/index-chart.js'
    self.target_paper = 'components/paper.html'
    self.target_tool = 'components/tool.html'
    self.target_statistic = 'components/statistic.html'
    self.target_statistic_js = 'assets/statistics-chart.js'

    # read all papers from the csv file
    self.papers = []
    with open(self.paper_filename, 'r') as file:
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

    # read all tools from the csv file
    self.tools = []
    with open(self.tools_filename, 'r') as file:
      for each in csv.DictReader(file):
        p = Tool(each)
        self.tools.append(p)

    print('[GenHTML] read {} papers, {} scholars, and {} tools'.format(
      len(self.papers), len(self.scholars), len(self.tools)))

  def generate_index(self, date):
    """
    Generate the static index.html file. Need to reaplce the followings:
    * Description of the sub-title <- last update date
    * Statistics <- number of papers, scholars, tools
    * Chart bar <- cumulative number of publications (with date)
    * Chart pie <- distribution of research topics
    """
    # update the HTML file 
    with open('pages/_index.html', 'r') as file:
      soup = BeautifulSoup(file.read(), 'html.parser')
    
    # description and statistics
    element = soup.find(id='replace-description')
    element.string = 'Collection of Research Papers and Tools of CIT (Last Update in {})'.format(date)
    element = soup.find(id='replace-number-1')  # papers
    element.string = '{}'.format(len(self.papers))
    element = soup.find(id='replace-number-2')  # scholars
    element.string = '{}'.format(len(self.scholars))
    element = soup.find(id='replace-number-3')  # tools
    element.string = '{}'.format(len(self.tools))
    element = soup.find(id='replace-bar-descrption')
    element.string = 'From 2000 to {}'.format(date.split()[-1])

    with open(self.target_index, 'w') as file:
      file.write(str(soup))
    
    # update the js file
    with open(self.target_index_js,'r') as f:
      lines = f.readlines()
    
    # cumulative number of publications
    lines[6] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['cumulative']['year']]))
    lines[12] = '        data: {}\n'.format(str(self.data['cumulative']['value']))
    
    # distribution of research fields
    lines[46] = '        data: {},\n'.format(str(self.data['distribution']['count']))
    lines[50] = '    labels: [{}]\n'.format(', '.join(['"{}"'.format(e) for e in self.data['distribution']['fields']]))

    with open(self.target_index_js, 'w') as f:
      f.writelines(lines)
    print('[GenHTML] update {} and {}'.format(self.target_index, self.target_index_js))

  def generate_papers_list(self):
    """
    Generate the paper page. Need to reaplce the followings:
    * Description of the sub-title <- number of papers
    * Data table <- complete paper list
    """
    # update the HTML file 
    with open('pages/_paper.html', 'r') as file:
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
      text_cell = BeautifulSoup('<td><p>{}<br><strong>{}</strong><br><em>{}</em></p></td>'.format(each.author, each.title, each.venue_str()), 'html.parser')
      doi_cell = BeautifulSoup(
        '<td><a href="https://www.doi.org/{}" target="_blank">DOI</a></td>'.format(
          each.doi), 'html.parser')

      new_row.append(name_cell)
      new_row.append(text_cell)
      new_row.append(doi_cell)
      element.append(new_row)
      # print(element)

    with open(self.target_paper, 'w') as file:
      file.write(str(soup))
    print('[GenHTML] add {} rows into {}'.format(len(self.papers), self.target_paper))

  def generate_statistics(self):
    """
    Generate the statistics page. Need to reaplce the followings:
    * Line chart <- annual number of publications
    * Bar chart <- distribution of publications on different research topics
    """
    # update the HTML file
    shutil.copyfile('pages/_statistic.html', self.target_statistic)

    # update the js file
    with open(self.target_statistic_js,'r') as f:
      lines = f.readlines()

    # annual number of publications
    lines[3] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['annual']['year']]))
    lines[9] = '        data: {}\n'.format(str(self.data['annual']['value']))

    # distribution of publications 
    lines[42] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['annual']['year']]))
    all_fields = ['Generation', 'Application', 'Evaluation', 'Optimization', 'Model', 'Diagnosis']
    for i, index in enumerate([46, 50, 54, 58, 62, 66]):
      field = all_fields[i]
      lines[index] = '          data: {}\n'.format(str(self.data['topic'][field]))

    with open(self.target_statistic_js, 'w') as f:
      f.writelines(lines)

    print('[GenHTML] update {} and {}'.format(self.target_statistic, self.target_statistic_js))

  def generate_tools_list(self):
    """
    Generate the tool page. Need to reaplce the followings:
    * Description of the sub-title <- number of tools
    * Data table <- complete tool list
    """
    # update the HTML file 
    with open('pages/_tool.html', 'r') as file:
      soup = BeautifulSoup(file.read(), 'html.parser')

    # replace "XX tools included"
    element = soup.find(id='replace-description')
    element.string = '{} tools that are publicly available'.format(len(self.tools))

    # replace data table 
    element = soup.find(id='replace-tool-data-tbody')
    element.string = ''

    # create a new row for each item in data and add this new row into the HTML table
    for each in self.tools:
      new_row = soup.new_tag('tr')
      name_cell = BeautifulSoup('<td><a href="{}">{}</a></td>'.format(each.link, each.name), 'html.parser')
      developer_cell = BeautifulSoup('<td>{}</td>'.format(each.developer), 'html.parser')
      release_cell = BeautifulSoup('<td>{}</td>'.format(each.release), 'html.parser')
      language_cell = BeautifulSoup('<td>{}</td>'.format(each.language), 'html.parser')
      algorithm_cell = BeautifulSoup('<td>{}</td>'.format(each.algorithm), 'html.parser')
      model_cell = BeautifulSoup('<td>{}</td>'.format(each.model), 'html.parser')
      constraint_cell = BeautifulSoup('<td>{}</td>'.format(each.constraint), 'html.parser')

      new_row.append(name_cell)
      new_row.append(developer_cell)
      new_row.append(release_cell)
      new_row.append(language_cell)
      new_row.append(algorithm_cell)
      new_row.append(model_cell)
      new_row.append(constraint_cell)
      element.append(new_row)
      # print(element)

    with open(self.target_tool, 'w') as file:
      file.write(str(soup))
    print('[GenHTML] add {} rows into {}'.format(len(self.tools), self.target_tool))

if __name__ == '__main__':
  g = Generator()
  g.generate_index(date='Jan 2025')
  g.generate_papers_list()
  g.generate_tools_list()
  g.generate_statistics()
