import csv
import pandas as pd
from bs4 import BeautifulSoup
from papers import Paper

csv_filename = 'data/list.csv'

def csv_sort():
  df = pd.read_csv(csv_filename, sep=',', header=0)
  df1 = df.sort_values('year', ascending=False)
  # print(df1)
  df1.to_csv(csv_filename, sep=',', encoding='utf-8', index=False, header=True)

def update_list():
  """
  Replace the table content of pages/_list.html with data in jsonfile
  The new HTML file will be saved as components/list.html
  """
  # read data from the json file
  data = []
  with open(csv_filename, 'r') as file:
    reader = csv.DictReader(file)
    for each in reader:
      p = Paper(each)
      data.append(p)
  print('[INFO] read {} papers from "{}"'.format(len(data), csv_filename))

  # read the template HTML file 
  with open('pages/_list.html', 'r') as file:
    text = file.read()

  soup = BeautifulSoup(text, 'html.parser')
  element = soup.find(id='paper-data-tbody')
  element.string = ''
  # print(element)

  # create a new row for each item in data
  # and add this new row into the HTML table
  for each in data:
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
  print('[INFO] succesfully add {} rows'.format(len(data)))

  # write the new HTML
  with open('components/list.html', 'w') as file:
    file.write(str(soup))
  print('[INFO] done')

if __name__ == '__main__':
  csv_sort()
  update_list()
