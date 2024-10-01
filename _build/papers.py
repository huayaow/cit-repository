import json

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
    self.json_data = js
 
  def __str__(self) -> str:
    return "{}\n{}\n{}\n".format(self.author, self.title, self.venue_str())

  def venue_str(self) -> str:
    venue = self.booktitle
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
  with open('_data/list_temp.json', 'r') as file:
    data = json.load(file)
    p = Paper(data[1])
    print(p)