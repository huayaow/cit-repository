class Scholar:
  def __init__(self, js) -> None:
    self.rank = js['rank'] if 'rank' in js.keys() else ''
    self.id = js['id']
    self.name = js['name']
    self.institution = js['institution']
    self.country = js['country']
    self.homepage = js['homepage']
    self.tse = js['TSE']
    self.tosem = js['TOSEM']
    self.emse = js['EMSE']
    self.jss = js['JSS']
    self.ist = js['IST']
    self.icse = js['ICSE']
    self.fse = js['FSE']
    self.ase = js['ASE']
    self.issta = js['ISSTA']
    self.saner = js['SANER']
    self.issre = js['ISSRE']
    self.icst = js['ICST']
    self.icstw = js['ICSTW']
    self.score = js['score'] if 'score' in js.keys() else ''
  
  def __str__(self) -> str:
    return "{}: {}, {}, score = {}".format(self.name, self.institution, 
                                           self.country, self.score)