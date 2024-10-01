class Paper:
  def __init__(self) -> None:
    self.year = ""
    self.type = ""
    self.author = ""
    self.title = ""
    self.field = ""
    self.tag = ""
    self.booktitle = ""
    self.abbr = ""
    self.vol = ""
    self.no = ""
    self.pages = ""
    self.doi = ""
    self.json_data = {}

  def read_from_json(self, js) -> None:
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
    return "{}\n{}\n{}\n".format(self.author, self.title, self.booktitle)

