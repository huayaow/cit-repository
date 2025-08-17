import csv
import json
from item.paper import Paper
from item.tool import Tool
from item.scholar import Scholar
from item.edge import Edge
from jinja2 import Environment, FileSystemLoader

class Data:
  def __init__(self):
    self.papers = []         # list of all papers
    self.scholars = []       # list of all scholars
    self.tools = []          # list of all tools
    self.statistics = None   # statistics data (json)
    self.rank = []           # list of ranked scholars

    paper_filename = 'data/paper.csv'
    scholar_filename = 'data/scholar.csv'
    tools_filename = 'data/tool.csv'
    statistics_filename = 'data/statistic.json'
    rank_filename = 'data/rank.csv'
    # co-authorship network
    node_filename = 'data/network/network_nodes.csv'
    edge_filename = 'data/network/network_edges.csv'
    centrality_filename = 'data/network/network_centrality.csv'

    with open(paper_filename, 'r') as file:
      self.papers = [Paper(each) for each in csv.DictReader(file)]
    
    with open(scholar_filename, 'r') as file:
      self.scholars = [Scholar(each) for each in csv.DictReader(file)]
    
    with open(tools_filename, 'r') as file:
      self.tools = [Tool(each) for each in csv.DictReader(file)]

    with open(statistics_filename) as file:
      self.statistics = json.load(file)

    with open(rank_filename, 'r') as file:
      self.rank = [Scholar(each) for each in csv.DictReader(file)]
    
    with open(node_filename, 'r') as file:
      self.network_nodes = [row for row in csv.DictReader(file)]

    with open(edge_filename, 'r') as file:
      self.network_edges = [Edge(row) for row in csv.DictReader(file)]

class Render:
  def __init__(self):
    self.env = Environment(loader = FileSystemLoader('templates'))
    self.data = Data()
    print('[Render] load data from files')

  def render(self, template_name, context, output_filename):
    template = self.env.get_template(template_name)
    html = template.render(context)
    with open(output_filename, 'w') as f:
      f.write(html)
  
  def render_all(self, update_date):
    self.render_index(update_date)
    self.render_paper()
    self.render_tool()
    self.render_statistic()
    self.render_rank()
    self.render_network()

  def render_index(self, update_date):
    """
    * basic descriptions <- Last update date, final year of bar chart
    * stat <- number of papers, scholars, tools
    * chart <- cumulative number of publications, and distribution of research topics
    """
    context = {
      'static_url': '',
      'active_page': 'home',
      'update_date': update_date,
      'final_year': self.data.statistics['cumulative-2000']['year'][-1],
      'stat': {
        "papers": len(self.data.papers),
        "scholars": len(self.data.scholars),
        "tools": len(self.data.tools)
      },
      'chart': {
        'bar': {
          'labels': self.data.statistics['cumulative-2000']['year'],
          'data': self.data.statistics['cumulative-2000']['value']
        },
        'pie': { 
          'labels': self.data.statistics['distribution']['fields'],
          'data': self.data.statistics['distribution']['count']
        }
      }
    }
    self.render('index.j2.html', context, 'index.html')
    self.render('index-chart.j2.js', context, 'assets/index-chart.js')
    print('[Render] generate index.html ({})'.format(update_date))

  def render_paper(self):
    context = {
      'static_url': '../',
      'active_page': 'paper',
      'paper_number': len(self.data.papers),
      'paper_list': self.data.papers
    }
    self.render('paper.j2.html', context, 'render/paper.html')
    print('[Render] generate paper.html ({} papers)'.format(context['paper_number']))
  
  def render_tool(self):
    context = {
      'static_url': '../',
      'active_page': 'tool',
      'tool_number': len(self.data.tools),
      'tool_list': self.data.tools
    }  
    self.render('tool.j2.html', context, 'render/tool.html')
    print('[Render] generate tool.html ({} tools)'.format(context['tool_number']))

  def render_statistic(self):
    context = {
      'static_url': '../',
      'active_page': 'statistic',
      'chart_annual': {
        'year': self.data.statistics['annual']['year'],
        'value': self.data.statistics['annual']['value']
      },
      'chart_topic': {
        'year': self.data.statistics['annual']['year'],
        'generation': self.data.statistics['topic']['Generation'],
        'application': self.data.statistics['topic']['Application'],
        'evaluation': self.data.statistics['topic']['Evaluation'],
        'optimization': self.data.statistics['topic']['Optimization'],
        'model': self.data.statistics['topic']['Model'],
        'diagnosis': self.data.statistics['topic']['Diagnosis']
      }
    }
    self.render('statistic.j2.html', context, 'render/statistic.html')
    self.render('statistic-chart.j2.js', context, 'assets/statistic-chart.js')
    print('[Render] generate statistic.html')

  def render_rank(self):
    context = {
      'static_url': '../',
      'active_page': 'rank',
      'scholar_list': self.data.rank
    }
    self.render('rank.j2.html', context, 'render/rank.html')
    print('[Render] generate rank.html')
  
  def render_network(self):
    context = {
      'static_url': '../',
      'active_page': 'network',
      'network_nodes': self.data.network_nodes,
      'network_edges': self.data.network_edges
    }
    self.render('network.j2.html', context, 'render/network.html')
    self.render('network-chart.j2.js', context, 'assets/network-chart.js')
    print('[Render] generate network.html')

if __name__ == '__main__':
  r = Render()
  r.render_all('Aug 2025')
