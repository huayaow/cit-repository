class Tool:
  def __init__(self, js) -> None:
    self.name = js['Name']
    self.developer = js['Developer']
    self.release = js['Release']
    self.language = '{} ({})'.format(js['Language'], js['Usage'])
    self.algorithm = js['Algorithm']
    self.model = js['Model']
    self.constraint = js['Constraint']
    self.link = js['Link']
  
  def __str__(self) -> str:
    return "{} @ {}".format(self.name, self.link)
