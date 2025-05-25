import csv 

class Paper:
  def __init__(self, js) -> None:
    self.year = js['year']
    self.type = js['type']
    self.author = js['author']
    self.title = js['title']
    self.field = js['field']
    self.tag = js['tag']
    self.booktitle = js['booktitle']
    self.abbr = js['abbr']
    self.vol = js['vol']
    self.no = js['no']
    self.pages = js['pages']
    self.doi = js['doi']
  
  def __str__(self) -> str:
    return "{}\n{}\n{}\n".format(self.author, self.title, self.venue_str())

  def venue_str(self) -> str:
    venue = self.booktitle
    if self.abbr != '':
      venue += ' ({})'.format(self.abbr)
    if self.type == 'inproceedings':
      venue += ', {}: {}'.format(self.year, self.pages)
    elif self.type == 'article':
      venue += ','
      if self.vol != '':
        venue += ' vol.{},'.format(self.vol)
      if self.no != '':
        venue += ' no.{},'.format(self.no)
      venue += ' pp.{}, {}'.format(self.pages, self.year)
    return venue

if __name__ == '__main__':
  with open('data/list.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)
  
  p = Paper(data[0])
  print(p)
