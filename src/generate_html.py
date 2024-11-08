import csv
import pandas as pd
from bs4 import BeautifulSoup
from papers import Paper

class Generator:
  def __init__(self, sort=False):
    self.list_filename = 'data/list.csv'
    self.scholar_filename = 'data/scholar.csv'

    # sort csv and get statistic data 
    self.data = self.read_csv(sort) 

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
    
    print('[INFO] read {} papers from "{}"'.format(len(self.papers), self.list_filename))
    print('       read {} scholars from "{}"'.format(len(self.scholars), self.scholar_filename))


  def read_csv(self, sort) -> dict:
    """
    Read csv file and calculate statistics for the basic BAR and PIE charts.
    """
    df = pd.read_csv(self.list_filename, sep=',', header=0)
    df = df.sort_values(['year', 'booktitle', 'title'], ascending=False)
    
    # cumulative number of publications
    bar_data = df.groupby('year').size().to_frame('number')
    bar_data['cumulative'] = bar_data['number'].cumsum()
    print(bar_data)

    # distribution of topics
    pie_data = df.groupby('field').size().to_frame('count')
    pie_data = pie_data.sort_values('count', ascending=False)
    print(pie_data)

    # final data
    data = {}
    year = bar_data.index.values.tolist()
    number = bar_data['number'].values.tolist()
    cumulative = bar_data['cumulative'].values.tolist()
    index = year.index(2000)    
    data['year'] = year[index:]
    data['number'] = number[index:]
    data['cumulative'] = cumulative[index:]
    data['fields'] = pie_data.index.values.tolist()
    data['count'] = pie_data['count'].values.tolist()

    if sort:
      df.to_csv(self.list_filename, sep=',', encoding='utf-8', index=False, header=True)

    return data

  def generate_index(self, date):
    """
    Generate the static index.html file. Need to reaplce the followings:
    * Description of the sub-title <- last update date
    * Statistics <- number of papers, [TODO: scholars, institutions]
    * Bar chart <- cumulative number of publications (with date)
    * Pie chart <- distribution of research topics
    """
    # read the template HTML file 
    with open('pages/_index.html', 'r') as file:
      text = file.read()

    soup = BeautifulSoup(text, 'html.parser')

    # description and statistics
    element = soup.find(id='replace-description')
    element.string = 'Collection of Research Papers of CIT (Last Update in {})'.format(date)

    element = soup.find(id='replace-number-1')
    element.string = '{}'.format(len(self.papers))

    element = soup.find(id='replace-number-2')
    element.string = '{}'.format(len(self.scholars))

    element = soup.find(id='replace-bar-descrption')
    element.string = 'From 2000 to {}'.format(date.split()[-1])
  
    # chart data
    with open('assets/index-chart.js','r') as f:
      lines = f.readlines()
    
    # bar chart
    lines[6] = '    labels: [{}],\n'.format(', '.join(['"{}"'.format(e) for e in self.data['year']]))
    lines[12] = '        data: {}\n'.format(str(self.data['cumulative']))
    # pie chart
    lines[46] = '        data: {},\n'.format(str(self.data['count']))
    lines[50] = '    labels: [{}]\n'.format(', '.join(['"{}"'.format(e) for e in self.data['fields']]))

    with open('assets/index-chart.js', 'w') as f:
      for line in lines:
        f.write(line)

    # write the new HTML
    with open('index.html', 'w') as file:
      file.write(str(soup))
    print('[INFO] succesfully update list.html"')


  def generate_list(self):
    """
    Generate the static components/list.html file. Need to reaplce the followings:
    * Description of the sub-title <- number of papers
    * Data table <- complete paper list
    """
    # read the template HTML file 
    with open('pages/_list.html', 'r') as file:
      text = file.read()

    soup = BeautifulSoup(text, 'html.parser')

    # replace "XX papers included"
    element = soup.find(id='replace-description')
    element.string = '{} papers included'.format(len(self.papers))

    # replace data table 
    element = soup.find(id='replace-paper-data-tbody')
    element.string = ''
    # print(element)

    # create a new row for each item in data
    # and add this new row into the HTML table
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

    # write the new HTML
    with open('components/list.html', 'w') as file:
      file.write(str(soup))
    print('[INFO] succesfully add {} rows into "components/list.html"'.format(len(self.papers)))

if __name__ == '__main__':
  g = Generator(sort=True)
  g.generate_index(date='Nov 2024')
  g.generate_list()
