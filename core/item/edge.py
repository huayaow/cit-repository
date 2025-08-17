class Edge:
  def __init__(self, js) -> None:
    self.source = js['source']
    self.target = js['target']
    self.weight = js['weight']

  def __str__(self) -> str:
    return "{} -> {} ({})".format(self.source, self.target, self.weight)
