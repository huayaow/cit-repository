from bs4 import BeautifulSoup

def update_all_paper_list():
  with open("components/list.html", "r") as f:
    text = f.read()

  soup = BeautifulSoup(text, 'html.parser')
  # print(soup.title)

  element = soup.find(id='paper-data-tbody')
  # print(element)

  # Create a new row
  new_row = soup.new_tag('tr')
  name_cell = soup.new_tag('td')
  name_cell.string = '2000'
  # age_cell = soup.new_tag('td')
  age_cell = BeautifulSoup('<td><p>Chuan Luo , Qiyuan Zhao , Shaowei Cai , Hongyu Zhang , Chunming Hu<br><strong>SamplingCA: effective and efficient sampling-based pairwise testing for highly XXXXX</strong><br><em>ACM Joint EuDDDDD, 2023: 1185--1197</em></p></td>', 'html.parser');
  doi_cell = soup.new_tag('td')
  doi_cell.string = 'DOI'

  # Append the new cells to the new row
  new_row.append(name_cell)
  new_row.append(age_cell)
  new_row.append(doi_cell)


  element.append(new_row)

  print(element)

  with open('components/updated_example.html', 'w') as file:
    file.write(str(soup))

if __name__ == '__main__':
  update_all_paper_list()